"""
Advanced String Formatter Module
==================================

This module provides an over-engineered string formatting system that employs
the Strategy Pattern to allow for flexible and extensible string transformations.

Key Features:
    - Abstract base classes for extensibility
    - Multiple concrete strategy implementations
    - Comprehensive type annotations
    - Detailed docstrings
    - Fluent interface support
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any, Callable, TypeVar
from enum import Enum
from dataclasses import dataclass
import re
import unicodedata


T = TypeVar("T", bound="StringFormatStrategy")


class CaseType(Enum):
    """Enumeration of available case transformations."""
    LOWER = "lower"
    UPPER = "upper"
    TITLE = "title"
    CAPITALIZE = "capitalize"
    SWAPCASE = "swapcase"
    CAMEL = "camel"
    SNAKE = "snake"
    PASCAL = "pascal"
    KEBAB = "kebab"


class WhitespaceMode(Enum):
    """Enumeration of whitespace normalization modes."""
    COMPRESS = "compress"
    TRIM = "trim"
    NORMALIZE = "normalize"
    REMOVE_ALL = "remove_all"
    PRESERVE = "preserve"


@dataclass
class StringFormatResult:
    """
    A data class representing the result of a string formatting operation.
    
    Attributes:
        success: Boolean indicating whether the operation succeeded
        result: The formatted string value
        original: The original input string
        transformations: List of transformations applied
        metadata: Additional metadata about the formatting operation
    """
    success: bool
    result: str
    original: str
    transformations: List[str]
    metadata: dict[str, Any]
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the result to a dictionary representation.
        
        Returns:
            dict[str, Any]: Dictionary representation of the result
        """
        return {
            "success": self.success,
            "result": self.result,
            "original": self.original,
            "transformations": self.transformations,
            "metadata": self.metadata
        }


class BaseStringFormatStrategy(ABC):
    """
    Abstract base class defining the contract for string formatting strategies.
    
    This class implements the Strategy Pattern, allowing different string
    transformation algorithms to be interchangeable.
    
    Attributes:
        priority: Priority level for strategy execution (lower = higher priority)
        enabled: Whether this strategy is currently enabled
    """
    
    def __init__(self, priority: int = 100, enabled: bool = True):
        """
        Initialize the strategy with priority and enabled state.
        
        Args:
            priority: Priority level (lower values execute first)
            enabled: Whether the strategy is enabled
        """
        self.priority = priority
        self.enabled = enabled
    
    @abstractmethod
    def apply(self, input_string: str, **kwargs) -> StringFormatResult:
        """
        Apply the string transformation to the input.
        
        Args:
            input_string: The string to transform
            **kwargs: Additional parameters for the transformation
            
        Returns:
            StringFormatResult: The result of the transformation
        """
        pass
    
    @abstractmethod
    def can_apply(self, input_string: str) -> bool:
        """
        Determine if this strategy can be applied to the input.
        
        Args:
            input_string: The string to check
            
        Returns:
            bool: True if the strategy can be applied
        """
        pass
    
    def __lt__(self, other: "BaseStringFormatStrategy") -> bool:
        """Compare strategies by priority for sorting."""
        return self.priority < other.priority


class CaseTransformationStrategy(BaseStringFormatStrategy):
    """
    A strategy for transforming the case of strings.
    
    Supports multiple case transformations including standard Python
    string methods and custom transformations like camelCase, snake_case, etc.
    """
    
    def __init__(self, case_type: Union[CaseType, str] = CaseType.TITLE):
        """
        Initialize the case transformation strategy.
        
        Args:
            case_type: The type of case transformation to apply
        """
        super().__init__(priority=10, enabled=True)
        if isinstance(case_type, str):
            case_type = CaseType(case_type.lower())
        self.case_type = case_type
    
    def apply(self, input_string: str, **kwargs) -> StringFormatResult:
        """
        Apply the case transformation to the input string.
        
        Args:
            input_string: The string to transform
            **kwargs: Additional parameters (not used in this strategy)
            
        Returns:
            StringFormatResult: The result of the transformation
        """
        original = input_string
        transformations = []
        
        try:
            if self.case_type == CaseType.LOWER:
                result = input_string.lower()
            elif self.case_type == CaseType.UPPER:
                result = input_string.upper()
            elif self.case_type == CaseType.TITLE:
                result = input_string.title()
            elif self.case_type == CaseType.CAPITALIZE:
                result = input_string.capitalize()
            elif self.case_type == CaseType.SWAPCASE:
                result = input_string.swapcase()
            elif self.case_type == CaseType.CAMEL:
                result = self._to_camel_case(input_string)
            elif self.case_type == CaseType.SNAKE:
                result = self._to_snake_case(input_string)
            elif self.case_type == CaseType.PASCAL:
                result = self._to_pascal_case(input_string)
            elif self.case_type == CaseType.KEBAB:
                result = self._to_kebab_case(input_string)
            else:
                raise ValueError(f"Unsupported case type: {self.case_type}")
            
            transformations.append(f"case_transform_{self.case_type.value}")
            
            return StringFormatResult(
                success=True,
                result=result,
                original=original,
                transformations=transformations,
                metadata={"case_type": self.case_type.value}
            )
        except Exception as e:
            return StringFormatResult(
                success=False,
                result=input_string,
                original=original,
                transformations=[],
                metadata={"error": str(e)}
            )
    
    def can_apply(self, input_string: str) -> bool:
        """
        Check if the strategy can be applied.
        
        Args:
            input_string: The string to check
            
        Returns:
            bool: Always True for case transformations
        """
        return isinstance(input_string, str) and len(input_string) > 0
    
    def _to_camel_case(self, input_string: str) -> str:
        """Convert string to camelCase."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        components = s2.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    def _to_snake_case(self, input_string: str) -> str:
        """Convert string to snake_case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.lower()
    
    def _to_pascal_case(self, input_string: str) -> str:
        """Convert string to PascalCase."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        return ''.join(x.title() for x in s2.split('_'))
    
    def _to_kebab_case(self, input_string: str) -> str:
        """Convert string to kebab-case."""
        return self._to_snake_case(input_string).replace('_', '-')


class WhitespaceNormalizationStrategy(BaseStringFormatStrategy):
    """
    A strategy for normalizing whitespace in strings.
    
    Supports multiple whitespace normalization modes including compression,
    trimming, and complete removal.
    """
    
    def __init__(self, mode: Union[WhitespaceMode, str] = WhitespaceMode.NORMALIZE):
        """
        Initialize the whitespace normalization strategy.
        
        Args:
            mode: The whitespace normalization mode
        """
        super().__init__(priority=20, enabled=True)
        if isinstance(mode, str):
            mode = WhitespaceMode(mode.lower())
        self.mode = mode
    
    def apply(self, input_string: str, **kwargs) -> StringFormatResult:
        """
        Apply whitespace normalization to the input string.
        
        Args:
            input_string: The string to normalize
            **kwargs: Additional parameters (not used in this strategy)
            
        Returns:
            StringFormatResult: The result of the normalization
        """
        original = input_string
        transformations = []
        
        try:
            if self.mode == WhitespaceMode.COMPRESS:
                result = re.sub(r'\s+', ' ', input_string)
            elif self.mode == WhitespaceMode.TRIM:
                result = input_string.strip()
            elif self.mode == WhitespaceMode.NORMALIZE:
                result = ' '.join(input_string.split())
            elif self.mode == WhitespaceMode.REMOVE_ALL:
                result = re.sub(r'\s+', '', input_string)
            elif self.mode == WhitespaceMode.PRESERVE:
                result = input_string
            else:
                raise ValueError(f"Unsupported whitespace mode: {self.mode}")
            
            transformations.append(f"whitespace_normalize_{self.mode.value}")
            
            return StringFormatResult(
                success=True,
                result=result,
                original=original,
                transformations=transformations,
                metadata={"mode": self.mode.value, "original_length": len(original)}
            )
        except Exception as e:
            return StringFormatResult(
                success=False,
                result=input_string,
                original=original,
                transformations=[],
                metadata={"error": str(e)}
            )
    
    def can_apply(self, input_string: str) -> bool:
        """
        Check if the strategy can be applied.
        
        Args:
            input_string: The string to check
            
        Returns:
            bool: Always True for whitespace normalization
        """
        return isinstance(input_string, str)


class EncodingTransformationStrategy(BaseStringFormatStrategy):
    """
    A strategy for transforming string encodings and unicode normalization.
    
    Supports unicode normalization (NFD, NFKD, NFC, NFKC) and encoding conversions.
    """
    
    class UnicodeForm(Enum):
        """Enumeration of unicode normalization forms."""
        NFD = "NFD"
        NFKD = "NFKD"
        NFC = "NFC"
        NFKC = "NFKC"
    
    def __init__(
        self,
        normalize_unicode: bool = True,
        unicode_form: Union[UnicodeForm, str] = UnicodeForm.NFC,
        remove_non_ascii: bool = False,
        remove_accents: bool = False
    ):
        """
        Initialize the encoding transformation strategy.
        
        Args:
            normalize_unicode: Whether to apply unicode normalization
            unicode_form: The unicode normalization form
            remove_non_ascii: Whether to remove non-ASCII characters
            remove_accents: Whether to remove diacritical marks
        """
        super().__init__(priority=30, enabled=True)
        self.normalize_unicode = normalize_unicode
        if isinstance(unicode_form, str):
            unicode_form = self.UnicodeForm(unicode_form.upper())
        self.unicode_form = unicode_form
        self.remove_non_ascii = remove_non_ascii
        self.remove_accents = remove_accents
    
    def apply(self, input_string: str, **kwargs) -> StringFormatResult:
        """
        Apply encoding transformations to the input string.
        
        Args:
            input_string: The string to transform
            **kwargs: Additional parameters (not used in this strategy)
            
        Returns:
            StringFormatResult: The result of the transformation
        """
        original = input_string
        transformations = []
        
        try:
            result = input_string
            
            if self.normalize_unicode:
                result = unicodedata.normalize(self.unicode_form.value, result)
                transformations.append(f"unicode_normalize_{self.unicode_form.value}")
            
            if self.remove_accents:
                result = unicodedata.normalize('NFD', result)
                result = ''.join(c for c in result if unicodedata.category(c) != 'Mn')
                transformations.append("remove_accents")
            
            if self.remove_non_ascii:
                result = ''.join(c for c in result if ord(c) < 128)
                transformations.append("remove_non_ascii")
            
            return StringFormatResult(
                success=True,
                result=result,
                original=original,
                transformations=transformations,
                metadata={
                    "normalize_unicode": self.normalize_unicode,
                    "unicode_form": self.unicode_form.value,
                    "remove_non_ascii": self.remove_non_ascii,
                    "remove_accents": self.remove_accents
                }
            )
        except Exception as e:
            return StringFormatResult(
                success=False,
                result=input_string,
                original=original,
                transformations=[],
                metadata={"error": str(e)}
            )
    
    def can_apply(self, input_string: str) -> bool:
        """
        Check if the strategy can be applied.
        
        Args:
            input_string: The string to check
            
        Returns:
            bool: Always True for encoding transformations
        """
        return isinstance(input_string, str)


class AdvancedStringFormatter:
    """
    An advanced string formatting engine that orchestrates multiple formatting strategies.
    
    This class uses the Chain of Responsibility pattern to apply multiple
    string transformations in a controlled manner.
    
    Example:
        >>> formatter = AdvancedStringFormatter()
        >>> formatter.add_strategy(CaseTransformationStrategy(CaseType.TITLE))
        >>> formatter.add_strategy(WhitespaceNormalizationStrategy(WhitespaceMode.NORMALIZE))
        >>> result = formatter.format("  hello WORLD  ")
        >>> print(result.result)
        "Hello World"
    """
    
    def __init__(self):
        """Initialize the formatter with an empty strategy list."""
        self._strategies: List[BaseStringFormatStrategy] = []
        self._enabled: bool = True
        self._transformation_log: List[StringFormatResult] = []
    
    def add_strategy(self, strategy: BaseStringFormatStrategy) -> "AdvancedStringFormatter":
        """
        Add a formatting strategy to the formatter.
        
        Args:
            strategy: The strategy to add
            
        Returns:
            AdvancedStringFormatter: Self for method chaining
        """
        if not isinstance(strategy, BaseStringFormatStrategy):
            raise TypeError("Strategy must be an instance of BaseStringFormatStrategy")
        self._strategies.append(strategy)
        self._strategies.sort()
        return self
    
    def remove_strategy(self, strategy: BaseStringFormatStrategy) -> "AdvancedStringFormatter":
        """
        Remove a formatting strategy from the formatter.
        
        Args:
            strategy: The strategy to remove
            
        Returns:
            AdvancedStringFormatter: Self for method chaining
        """
        if strategy in self._strategies:
            self._strategies.remove(strategy)
        return self
    
    def clear_strategies(self) -> "AdvancedStringFormatter":
        """
        Clear all formatting strategies.
        
        Returns:
            AdvancedStringFormatter: Self for method chaining
        """
        self._strategies.clear()
        return self
    
    def format(self, input_string: str, **kwargs) -> StringFormatResult:
        """
        Apply all enabled strategies to the input string.
        
        Args:
            input_string: The string to format
            **kwargs: Additional parameters passed to strategies
            
        Returns:
            StringFormatResult: The final formatted result
        """
        if not self._enabled:
            return StringFormatResult(
                success=True,
                result=input_string,
                original=input_string,
                transformations=[],
                metadata={"message": "Formatter is disabled"}
            )
        
        current_string = input_string
        all_transformations = []
        metadata = {"input_length": len(input_string)}
        
        for strategy in self._strategies:
            if not strategy.enabled or not strategy.can_apply(current_string):
                continue
            
            result = strategy.apply(current_string, **kwargs)
            
            if result.success:
                current_string = result.result
                all_transformations.extend(result.transformations)
                metadata.update(result.metadata)
            else:
                self._transformation_log.append(result)
        
        final_result = StringFormatResult(
            success=True,
            result=current_string,
            original=input_string,
            transformations=all_transformations,
            metadata=metadata
        )
        
        self._transformation_log.append(final_result)
        return final_result
    
    def format_batch(
        self,
        input_strings: List[str],
        **kwargs
    ) -> List[StringFormatResult]:
        """
        Format multiple strings in batch.
        
        Args:
            input_strings: List of strings to format
            **kwargs: Additional parameters passed to strategies
            
        Returns:
            List[StringFormatResult]: List of formatted results
        """
        return [self.format(s, **kwargs) for s in input_strings]
    
    def get_transformation_log(self) -> List[StringFormatResult]:
        """
        Get the log of all transformations performed.
        
        Returns:
            List[StringFormatResult]: List of transformation results
        """
        return self._transformation_log.copy()
    
    def clear_transformation_log(self) -> None:
        """Clear the transformation log."""
        self._transformation_log.clear()
    
    def enable(self) -> "AdvancedStringFormatter":
        """
        Enable the formatter.
        
        Returns:
            AdvancedStringFormatter: Self for method chaining
        """
        self._enabled = True
        return self
    
    def disable(self) -> "AdvancedStringFormatter":
        """
        Disable the formatter.
        
        Returns:
            AdvancedStringFormatter: Self for method chaining
        """
        self._enabled = False
        return self
    
    def is_enabled(self) -> bool:
        """
        Check if the formatter is enabled.
        
        Returns:
            bool: True if enabled
        """
        return self._enabled
    
    def __len__(self) -> int:
        """Return the number of registered strategies."""
        return len(self._strategies)
    
    def __repr__(self) -> str:
        """Return a string representation of the formatter."""
        enabled_strategies = sum(1 for s in self._strategies if s.enabled)
        return (f"AdvancedStringFormatter(strategies={len(self._strategies)}, "
                f"enabled={enabled_strategies}, formatter_enabled={self._enabled})")


# Type aliases for backward compatibility
StringFormatStrategy = BaseStringFormatStrategy
