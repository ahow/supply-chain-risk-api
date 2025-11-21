"""
I-O Model Factory

This module provides a factory for creating I-O model instances based on user selection.
"""

from typing import Optional, List, Dict
from io_model_base import IOModel
from oecd_icio_model import OECDICIOModel
from exiobase_model import EXIOBASEModel


class IOModelFactory:
    """
    Factory for creating I-O model instances.
    
    Supports multiple I-O databases and provides a unified interface
    for model selection and instantiation.
    """
    
    # Available models
    MODELS = {
        'oecd': {
            'class': OECDICIOModel,
            'name': 'OECD ICIO Extended',
            'description': 'Best for broad geographic coverage (85 countries)',
            'strengths': [
                '85 countries including extensive developing country coverage',
                '56 sectors (ISIC Rev. 4)',
                'Firm heterogeneity for China and Mexico',
                'Most recent data: 2020'
            ],
            'use_cases': [
                'Sourcing from developing countries (Bangladesh, Ethiopia, Nigeria, etc.)',
                'Broad geographic risk analysis',
                'Country-specific supply chain mapping',
                'Trade policy analysis'
            ]
        },
        'exiobase': {
            'class': EXIOBASEModel,
            'name': 'EXIOBASE 3',
            'description': 'Best for detailed sector analysis and environmental data',
            'strengths': [
                '49 regions (44 countries + 5 Rest of World)',
                '163 industries (mapped to OECD sectors)',
                '2,720+ environmental indicators',
                'Most recent data: 2022'
            ],
            'use_cases': [
                'Detailed manufacturing supply chain analysis',
                'Environmental footprint assessment',
                'Sector-specific risk analysis',
                'Carbon/water/land footprint calculations'
            ],
            'status': 'Partially implemented - coefficient matrix pending'
        }
    }
    
    # Default model
    DEFAULT_MODEL = 'oecd'
    
    @classmethod
    def create_model(cls, model_type: str = None, **kwargs) -> IOModel:
        """
        Create an I-O model instance.
        
        Args:
            model_type: Type of model to create ('oecd', 'exiobase', etc.)
                       If None, uses default model
            **kwargs: Additional arguments passed to model constructor
            
        Returns:
            IOModel instance
            
        Raises:
            ValueError: If model_type is not supported
        """
        if model_type is None:
            model_type = cls.DEFAULT_MODEL
        
        model_type = model_type.lower()
        
        if model_type not in cls.MODELS:
            available = ', '.join(cls.MODELS.keys())
            raise ValueError(
                f"Unknown model type: '{model_type}'. "
                f"Available models: {available}"
            )
        
        model_class = cls.MODELS[model_type]['class']
        return model_class(**kwargs)
    
    @classmethod
    def get_available_models(cls) -> List[Dict]:
        """
        Get list of available I-O models with their metadata.
        
        Returns:
            List of dictionaries containing model information
        """
        models = []
        for model_id, model_info in cls.MODELS.items():
            models.append({
                'id': model_id,
                'name': model_info['name'],
                'description': model_info['description'],
                'strengths': model_info['strengths'],
                'use_cases': model_info['use_cases'],
                'status': model_info.get('status', 'Available')
            })
        return models
    
    @classmethod
    def get_model_info(cls, model_type: str) -> Optional[Dict]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_type: Type of model ('oecd', 'exiobase', etc.)
            
        Returns:
            Dictionary with model information, or None if not found
        """
        model_type = model_type.lower()
        if model_type in cls.MODELS:
            info = cls.MODELS[model_type].copy()
            info['id'] = model_type
            return info
        return None
    
    @classmethod
    def recommend_model(
        cls,
        country: Optional[str] = None,
        needs_environmental_data: bool = False,
        needs_sector_detail: bool = False
    ) -> str:
        """
        Recommend the best model based on user requirements.
        
        Args:
            country: Country code (if specific country is needed)
            needs_environmental_data: Whether environmental data is required
            needs_sector_detail: Whether detailed sector breakdown is needed
            
        Returns:
            Recommended model type ('oecd' or 'exiobase')
        """
        # If environmental data is needed, recommend EXIOBASE
        if needs_environmental_data:
            return 'exiobase'
        
        # If detailed sector breakdown is needed, recommend EXIOBASE
        if needs_sector_detail:
            return 'exiobase'
        
        # Check if country is available in both models
        if country:
            # For now, default to OECD for country-specific queries
            # (would need to check actual country availability in production)
            return 'oecd'
        
        # Default recommendation
        return cls.DEFAULT_MODEL
    
    @classmethod
    def validate_model_type(cls, model_type: str) -> bool:
        """
        Check if a model type is valid.
        
        Args:
            model_type: Model type to validate
            
        Returns:
            True if valid, False otherwise
        """
        return model_type.lower() in cls.MODELS


# Convenience function for creating models
def create_io_model(model_type: str = None, **kwargs) -> IOModel:
    """
    Convenience function to create an I-O model.
    
    Args:
        model_type: Type of model ('oecd', 'exiobase', etc.)
        **kwargs: Additional arguments for model constructor
        
    Returns:
        IOModel instance
    """
    return IOModelFactory.create_model(model_type, **kwargs)
