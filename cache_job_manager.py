"""Background Job Manager for Cache Refresh

Manages long-running cache refresh operations that exceed HTTP timeout limits.
Uses threading to run cache population in the background while returning immediately.
"""
import threading
import time
from typing import Dict, Optional
from datetime import datetime


class CacheJobManager:
    """Manages background cache refresh jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}
        self.current_job_id: Optional[str] = None
        self.lock = threading.Lock()
    
    def start_job(self, job_id: str, country_list: list, force_refresh: bool = False) -> Dict:
        """Start a cache refresh job in the background
        
        Args:
            job_id: Unique identifier for the job
            country_list: List of country names to process
            force_refresh: If True, refresh all countries even if cached
        
        Returns:
            Job status dictionary
        """
        with self.lock:
            # Check if a job is already running
            if self.current_job_id and self.jobs[self.current_job_id]['status'] == 'running':
                return {
                    'error': 'A cache refresh job is already running',
                    'current_job_id': self.current_job_id,
                    'current_job': self.jobs[self.current_job_id]
                }
            
            # Create new job
            self.jobs[job_id] = {
                'job_id': job_id,
                'status': 'running',
                'started_at': datetime.utcnow().isoformat(),
                'completed_at': None,
                'progress': {
                    'total': len(country_list),
                    'processed': 0,
                    'success': 0,
                    'failed': 0,
                    'skipped': 0,
                    'current_country': None
                },
                'results': None,
                'error': None
            }
            
            self.current_job_id = job_id
            
            # Start background thread
            thread = threading.Thread(
                target=self._run_cache_refresh,
                args=(job_id, country_list, force_refresh),
                daemon=True
            )
            thread.start()
            
            return self.jobs[job_id]
    
    def _run_cache_refresh(self, job_id: str, country_list: list, force_refresh: bool):
        """Run cache refresh in background thread"""
        from expected_loss_cache import get_cache
        
        try:
            cache = get_cache()
            
            # Clear cache if force refresh
            if force_refresh:
                cache.cache = {}
            
            # Process each country
            for i, country_name in enumerate(country_list, 1):
                with self.lock:
                    self.jobs[job_id]['progress']['current_country'] = country_name
                    self.jobs[job_id]['progress']['processed'] = i
                
                # Skip if already cached and not force refresh
                if not force_refresh and country_name in cache.cache:
                    with self.lock:
                        self.jobs[job_id]['progress']['skipped'] += 1
                    continue
                
                # Fetch and cache
                result = cache.populate_country(country_name)
                
                with self.lock:
                    if result == 'success':
                        self.jobs[job_id]['progress']['success'] += 1
                    elif result == 'skipped':
                        self.jobs[job_id]['progress']['skipped'] += 1
                    else:  # 'failed'
                        self.jobs[job_id]['progress']['failed'] += 1
            
            # Save cache
            cache.save_cache()
            
            # Mark job as completed
            with self.lock:
                self.jobs[job_id]['status'] = 'completed'
                self.jobs[job_id]['completed_at'] = datetime.utcnow().isoformat()
                self.jobs[job_id]['results'] = {
                    'total': self.jobs[job_id]['progress']['total'],
                    'success': self.jobs[job_id]['progress']['success'],
                    'failed': self.jobs[job_id]['progress']['failed'],
                    'skipped': self.jobs[job_id]['progress']['skipped']
                }
                self.jobs[job_id]['progress']['current_country'] = None
                
                if self.current_job_id == job_id:
                    self.current_job_id = None
        
        except Exception as e:
            with self.lock:
                self.jobs[job_id]['status'] = 'failed'
                self.jobs[job_id]['completed_at'] = datetime.utcnow().isoformat()
                self.jobs[job_id]['error'] = str(e)
                
                if self.current_job_id == job_id:
                    self.current_job_id = None
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get status of a specific job"""
        with self.lock:
            return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> Dict:
        """Get status of all jobs"""
        with self.lock:
            return {
                'current_job_id': self.current_job_id,
                'jobs': list(self.jobs.values())
            }
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job (best effort - thread may not stop immediately)"""
        with self.lock:
            if job_id in self.jobs and self.jobs[job_id]['status'] == 'running':
                self.jobs[job_id]['status'] = 'cancelled'
                self.jobs[job_id]['completed_at'] = datetime.utcnow().isoformat()
                
                if self.current_job_id == job_id:
                    self.current_job_id = None
                
                return True
            return False


# Global job manager instance
_job_manager = None

def get_job_manager() -> CacheJobManager:
    """Get or create global job manager instance"""
    global _job_manager
    if _job_manager is None:
        _job_manager = CacheJobManager()
    return _job_manager
