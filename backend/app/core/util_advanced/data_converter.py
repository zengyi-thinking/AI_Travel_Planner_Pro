"""
Redundant Data Converter Module
================================

This module provides an over-engineered data conversion system that supports
multiple type conversions, format transformations, and encoding conversions.

Key Features:
    - Abstract base classes for extensibility
    - Support for type, format, and encoding conversions
    - Comprehensive type annotations with Union types
    - Detailed docstrings
    - Conversion validation and error handling
"""

from abc import ABC, abstractmethod
from typing import List, Union, Optional, Any, Type, TypeVar, Dict, Callable, Generic
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import base64
import uuid
import hashlib


T = TypeVar("T")
SourceType = TypeVar("SourceType")
TargetType = TypeVar("TargetType")


class ConversionType(Enum):
    """Enumeration of supported conversion types."""
    # Type conversions
    INT = "int"
    FLOAT = "float"
    STR = "str"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    TUPLE = "tuple"
    SET = "set"
    
    # Format conversions
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    YAML = "yaml"
    
    # Encoding conversions
    BASE64 = "base64"
    HEX = "hex"
    URL = "url"
    UNICODE = "unicode"


@dataclass
class ConversionResult:
    """
    A data class representing the result of a data conversion operation.
    
    Attributes:
        success: Boolean indicating whether the conversion succeeded
        value: The converted value
        original: The original input value
        source_type: The type of the original value
        target_type: The type of the converted value
        conversion_type: The type of conversion performed
        steps: List of conversion steps taken
        metadata: Additional metadata about the conversion
    """
    success: bool
    value: Any
    original: Any
    source_type: str
    target_type: str
    conversion_type: ConversionType
    steps: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the result
        """
        return {
            "success": self.success,
            "value": str(self.value) if not isinstance(self.value, (dict, list)) else self.value,
            "original": str(self.original),
            "source_type": self.source_type,
            "target_type": self.target_type,
            "conversion_type": self.conversion_type.value,
            "steps": self.steps,
            "metadata": self.metadata
        }
    
    def __repr__(self) -> str:
        """Return a string representation of the result."""
        if self.success:
            return (f"ConversionResult(success=True, source={self.source_type}, "
                    f"target={self.target_type}, value={self.value})")
        return (f"ConversionResult(success=False, source={self.source_type}, "
                f"target={self.target_type}, error={self.metadata.get('error', 'Unknown')})")


class BaseConversionStrategy(ABC, Generic[SourceType, TargetType]):
    """
    Abstract base class defining the contract for data conversion strategies.
    
    This class implements the Strategy Pattern, allowing different
    conversion algorithms to be interchangeable.
    
    Attributes:
        conversion_type: The type of conversion
        enabled: Whether this strategy is currently enabled
        priority: Priority level for strategy execution
    """
    
    def __init__(
        self,
        conversion_type: ConversionType,
        enabled: bool = True,
        priority: int = 100
    ):
        """
        Initialize the conversion strategy.
        
        Args:
            conversion_type: The type of conversion
            enabled: Whether the strategy is enabled
            priority: Priority level (lower values execute first)
        """
        self.conversion_type = conversion_type
        self.enabled = enabled
        self.priority = priority
    
    @abstractmethod
    def convert(self, input_value: SourceType, **kwargs) -> ConversionResult:
        """
        Perform the data conversion.
        
        Args:
            input_value: The value to convert
            **kwargs: Additional parameters for the conversion
            
        Returns:
            ConversionResult: The result of the conversion
        """
        pass
    
    @abstractmethod
    def can_convert(self, input_value: Any) -> bool:
        """
        Determine if this strategy can convert the input.
        
        Args:
            input_value: The value to check
            
        Returns:
            bool: True if the strategy can convert the value
        """
        pass
    
    def _get_type_name(self, value: Any) -> str:
        """
        Get the type name of a value.
        
        Args:
            value: The value to check
            
        Returns:
            str: The type name
        """
        return type(value).__name__
    
    def __lt__(self, other: "BaseConversionStrategy") -> bool:
        """Compare strategies by priority for sorting."""
        return self.priority < other.priority


class TypeConversionStrategy(BaseConversionStrategy):
    """
    A strategy for performing type conversions between basic Python types.
    
    Supports conversions between int, float, str, bool, list, dict, tuple, and set.
    """
    
    def __init__(
        self,
        target_type: Union[ConversionType, str],
        enabled: bool = True,
        priority: int = 10
    ):
        """
        Initialize the type conversion strategy.
        
        Args:
            target_type: The target type to convert to
            enabled: Whether the strategy is enabled
            priority: Priority level for strategy execution
        """
        if isinstance(target_type, str):
            target_type = ConversionType(target_type.lower())
        
        # Validate that it's a type conversion
        type_conversions = {
            ConversionType.INT, ConversionType.FLOAT, ConversionType.STR,
            ConversionType.BOOL, ConversionType.LIST, ConversionType.DICT,
            ConversionType.TUPLE, ConversionType.SET
        }
        
        if target_type not in type_conversions:
            raise ValueError(f"Invalid type conversion target: {target_type}")
        
        super().__init__(target_type, enabled, priority)
        self.target_type = target_type
    
    def convert(self, input_value: Any, **kwargs) -> ConversionResult:
        """
        Perform the type conversion.
        
        Args:
            input_value: The value to convert
            **kwargs: Additional parameters (e.g., encoding for str conversion)
            
        Returns:
            ConversionResult: The result of the conversion
        """
        original = input_value
        source_type = self._get_type_name(input_value)
        steps = []
        
        try:
            if self.target_type == ConversionType.INT:
                result = self._to_int(input_value, **kwargs)
            elif self.target_type == ConversionType.FLOAT:
                result = self._to_float(input_value, **kwargs)
            elif self.target_type == ConversionType.STR:
                result = self._to_str(input_value, **kwargs)
            elif self.target_type == ConversionType.BOOL:
                result = self._to_bool(input_value, **kwargs)
            elif self.target_type == ConversionType.LIST:
                result = self._to_list(input_value, **kwargs)
            elif self.target_type == ConversionType.DICT:
                result = self._to_dict(input_value, **kwargs)
            elif self.target_type == ConversionType.TUPLE:
                result = self._to_tuple(input_value, **kwargs)
            elif self.target_type == ConversionType.SET:
                result = self._to_set(input_value, **kwargs)
            else:
                raise ValueError(f"Unsupported target type: {self.target_type}")
            
            target_type = self._get_type_name(result)
            steps.append(f"type_conversion_{self.target_type.value}")
            
            return ConversionResult(
                success=True,
                value=result,
                original=original,
                source_type=source_type,
                target_type=target_type,
                conversion_type=self.target_type,
                steps=steps,
                metadata={"conversion_method": "type_cast"}
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                value=original,
                original=original,
                source_type=source_type,
                target_type=self.target_type.value,
                conversion_type=self.target_type,
                steps=[],
                metadata={"error": str(e)}
            )
    
    def can_convert(self, input_value: Any) -> bool:
        """
        Check if the strategy can convert the input.
        
        Args:
            input_value: The value to check
            
        Returns:
            bool: True if the strategy can convert the value
        """
        return True
    
    def _to_int(self, value: Any, **kwargs) -> int:
        """Convert value to int."""
        if isinstance(value, str):
            value = value.strip()
            return int(value, 0 if value.startswith(("0x", "0b", "0o")) else 10)
        return int(value)
    
    def _to_float(self, value: Any, **kwargs) -> float:
        """Convert value to float."""
        return float(value)
    
    def _to_str(self, value: Any, **kwargs) -> str:
        """Convert value to str."""
        encoding = kwargs.get("encoding", "utf-8")
        if isinstance(value, bytes):
            return value.decode(encoding)
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)
    
    def _to_bool(self, value: Any, **kwargs) -> bool:
        """Convert value to bool."""
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "y", "on")
        if isinstance(value, (int, float)):
            return value != 0
        return bool(value)
    
    def _to_list(self, value: Any, **kwargs) -> list:
        """Convert value to list."""
        if isinstance(value, str):
            return list(value)
        if isinstance(value, (dict, set, tuple)):
            return list(value)
        if hasattr(value, "__iter__") and not isinstance(value, str):
            return list(value)
        return [value]
    
    def _to_dict(self, value: Any, **kwargs) -> dict:
        """Convert value to dict."""
        if isinstance(value, dict):
            return dict(value)
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {"value": value}
        raise ValueError(f"Cannot convert {type(value).__name__} to dict")
    
    def _to_tuple(self, value: Any, **kwargs) -> tuple:
        """Convert value to tuple."""
        if isinstance(value, str):
            return tuple(value)
        if isinstance(value, (list, set)):
            return tuple(value)
        if hasattr(value, "__iter__") and not isinstance(value, str):
            return tuple(value)
        return (value,)
    
    def _to_set(self, value: Any, **kwargs) -> set:
        """Convert value to set."""
        if isinstance(value, str):
            return set(value)
        if isinstance(value, (list, tuple)):
            return set(value)
        if hasattr(value, "__iter__") and not isinstance(value, str):
            return set(value)
        return {value}


class FormatConversionStrategy(BaseConversionStrategy):
    """
    A strategy for performing format conversions between different data formats.
    
    Supports conversions between JSON, XML, CSV, and YAML formats.
    """
    
    def __init__(
        self,
        target_format: Union[ConversionType, str],
        enabled: bool = True,
        priority: int = 20
    ):
        """
        Initialize the format conversion strategy.
        
        Args:
            target_format: The target format to convert to
            enabled: Whether the strategy is enabled
            priority: Priority level for strategy execution
        """
        if isinstance(target_format, str):
            target_format = ConversionType(target_format.lower())
        
        # Validate that it's a format conversion
        format_conversions = {
            ConversionType.JSON, ConversionType.XML,
            ConversionType.CSV, ConversionType.YAML
        }
        
        if target_format not in format_conversions:
            raise ValueError(f"Invalid format conversion target: {target_format}")
        
        super().__init__(target_format, enabled, priority)
        self.target_format = target_format
    
    def convert(self, input_value: Any, **kwargs) -> ConversionResult:
        """
        Perform the format conversion.
        
        Args:
            input_value: The value to convert
            **kwargs: Additional parameters (e.g., indent for JSON)
            
        Returns:
            ConversionResult: The result of the conversion
        """
        original = input_value
        source_type = self._get_type_name(input_value)
        steps = []
        
        try:
            if self.target_format == ConversionType.JSON:
                result = self._to_json(input_value, **kwargs)
            elif self.target_format == ConversionType.XML:
                result = self._to_xml(input_value, **kwargs)
            elif self.target_format == ConversionType.CSV:
                result = self._to_csv(input_value, **kwargs)
            elif self.target_format == ConversionType.YAML:
                result = self._to_yaml(input_value, **kwargs)
            else:
                raise ValueError(f"Unsupported target format: {self.target_format}")
            
            target_type = "str"
            steps.append(f"format_conversion_{self.target_format.value}")
            
            return ConversionResult(
                success=True,
                value=result,
                original=original,
                source_type=source_type,
                target_type=target_type,
                conversion_type=self.target_format,
                steps=steps,
                metadata={"conversion_method": "format_serializer"}
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                value=original,
                original=original,
                source_type=source_type,
                target_type=self.target_format.value,
                conversion_type=self.target_format,
                steps=[],
                metadata={"error": str(e)}
            )
    
    def can_convert(self, input_value: Any) -> bool:
        """
        Check if the strategy can convert the input.
        
        Args:
            input_value: The value to check
            
        Returns:
            bool: True if the strategy can convert the value
        """
        return isinstance(input_value, (dict, list, str))
    
    def _to_json(self, value: Any, **kwargs) -> str:
        """Convert value to JSON format."""
        indent = kwargs.get("indent", 2)
        ensure_ascii = kwargs.get("ensure_ascii", False)
        if isinstance(value, str):
            value = json.loads(value)
        return json.dumps(value, indent=indent, ensure_ascii=ensure_ascii)
    
    def _to_xml(self, value: Any, **kwargs) -> str:
        """Convert value to XML format."""
        root_tag = kwargs.get("root_tag", "root")
        indent = kwargs.get("indent", 2)
        
        def dict_to_xml(d: dict, parent: str) -> str:
            """Recursively convert dictionary to XML."""
            xml_parts = []
            for key, val in d.items():
                if isinstance(val, dict):
                    xml_parts.append(f"<{key}>{dict_to_xml(val, key)}</{key}>")
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            xml_parts.append(f"<{key}>{dict_to_xml(item, key)}</{key}>")
                        else:
                            xml_parts.append(f"<{key}>{item}</{key}>")
                else:
                    xml_parts.append(f"<{key}>{val}</{key}>")
            return "".join(xml_parts)
        
        if isinstance(value, str):
            value = json.loads(value)
        
        if isinstance(value, dict):
            return f"<{root_tag}>{dict_to_xml(value, root_tag)}</{root_tag}>"
        else:
            return f"<{root_tag}>{value}</{root_tag}>"
    
    def _to_csv(self, value: Any, **kwargs) -> str:
        """Convert value to CSV format."""
        delimiter = kwargs.get("delimiter", ",")
        newline = kwargs.get("newline", "\n")
        
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                # Assume it's already a CSV string
                return value
        
        if isinstance(value, list):
            if all(isinstance(row, (list, tuple)) for row in value):
                return newline.join(delimiter.join(str(cell) for cell in row) for row in value)
            else:
                return newline.join(str(item) for item in value)
        
        if isinstance(value, dict):
            return newline.join(f"{k}{delimiter}{v}" for k, v in value.items())
        
        raise ValueError(f"Cannot convert {type(value).__name__} to CSV")
    
    def _to_yaml(self, value: Any, **kwargs) -> str:
        """Convert value to YAML format."""
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
        
        def to_yaml_string(val: Any, indent: int = 0) -> str:
            """Recursively convert value to YAML string."""
            prefix = "  " * indent
            if isinstance(val, dict):
                return "\n".join(
                    f"{prefix}{k}: {to_yaml_string(v, indent + 1)}" 
                    for k, v in val.items()
                )
            elif isinstance(val, (list, tuple)):
                return "\n".join(f"{prefix}- {to_yaml_string(item, indent + 1)}" for item in val)
            else:
                return str(val)
        
        return to_yaml_string(value)


class EncodingConversionStrategy(BaseConversionStrategy):
    """
    A strategy for performing encoding conversions.
    
    Supports conversions between plain text, Base64, hexadecimal, URL encoding,
    and Unicode encoding.
    """
    
    def __init__(
        self,
        target_encoding: Union[ConversionType, str],
        enabled: bool = True,
        priority: int = 30
    ):
        """
        Initialize the encoding conversion strategy.
        
        Args:
            target_encoding: The target encoding to convert to
            enabled: Whether the strategy is enabled
            priority: Priority level for strategy execution
        """
        if isinstance(target_encoding, str):
            target_encoding = ConversionType(target_encoding.lower())
        
        # Validate that it's an encoding conversion
        encoding_conversions = {
            ConversionType.BASE64, ConversionType.HEX,
            ConversionType.URL, ConversionType.UNICODE
        }
        
        if target_encoding not in encoding_conversions:
            raise ValueError(f"Invalid encoding conversion target: {target_encoding}")
        
        super().__init__(target_encoding, enabled, priority)
        self.target_encoding = target_encoding
    
    def convert(self, input_value: Any, **kwargs) -> ConversionResult:
        """
        Perform the encoding conversion.
        
        Args:
            input_value: The value to convert
            **kwargs: Additional parameters (e.g., encoding for str conversion)
            
        Returns:
            ConversionResult: The result of the conversion
        """
        original = input_value
        source_type = self._get_type_name(input_value)
        steps = []
        
        try:
            # Convert input to string if necessary
            if isinstance(input_value, bytes):
                string_value = input_value.decode(kwargs.get("encoding", "utf-8"))
                steps.append("bytes_to_string")
            elif isinstance(input_value, str):
                string_value = input_value
            else:
                string_value = str(input_value)
                steps.append("to_string")
            
            if self.target_encoding == ConversionType.BASE64:
                result = self._to_base64(string_value)
            elif self.target_encoding == ConversionType.HEX:
                result = self._to_hex(string_value)
            elif self.target_encoding == ConversionType.URL:
                result = self._to_url(string_value)
            elif self.target_encoding == ConversionType.UNICODE:
                result = self._to_unicode(string_value)
            else:
                raise ValueError(f"Unsupported target encoding: {self.target_encoding}")
            
            target_type = "str"
            steps.append(f"encoding_conversion_{self.target_encoding.value}")
            
            return ConversionResult(
                success=True,
                value=result,
                original=original,
                source_type=source_type,
                target_type=target_type,
                conversion_type=self.target_encoding,
                steps=steps,
                metadata={"conversion_method": "encoding_transform"}
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                value=original,
                original=original,
                source_type=source_type,
                target_type=self.target_encoding.value,
                conversion_type=self.target_encoding,
                steps=[],
                metadata={"error": str(e)}
            )
    
    def can_convert(self, input_value: Any) -> bool:
        """
        Check if the strategy can convert the input.
        
        Args:
            input_value: The value to check
            
        Returns:
            bool: True if the strategy can convert the value
        """
        return isinstance(input_value, (str, bytes, int, float))
    
    def _to_base64(self, value: str) -> str:
        """Convert value to Base64 encoding."""
        return base64.b64encode(value.encode("utf-8")).decode("ascii")
    
    def _to_hex(self, value: str) -> str:
        """Convert value to hexadecimal encoding."""
        return value.encode("utf-8").hex()
    
    def _to_url(self, value: str) -> str:
        """Convert value to URL encoding."""
        from urllib.parse import quote
        return quote(value, safe="")
    
    def _to_unicode(self, value: str) -> str:
        """Convert value to Unicode escape sequence."""
        return "".join(f"\\u{ord(c):04x}" for c in value)


class RedundantDataConverter:
    """
    An advanced data conversion engine that orchestrates multiple conversion strategies.
    
    This class uses the Chain of Responsibility pattern to apply multiple
    data conversions in a controlled manner.
    
    Example:
        >>> converter = RedundantDataConverter()
        >>> converter.add_strategy(TypeConversionStrategy(ConversionType.INT))
        >>> converter.add_strategy(EncodingConversionStrategy(ConversionType.BASE64))
        >>> result = converter.convert("123")
        >>> print(result.value)
        "MTIz"
    """
    
    def __init__(self):
        """Initialize the converter with an empty strategy list."""
        self._strategies: List[BaseConversionStrategy] = []
        self._enabled: bool = True
        self._conversion_log: List[ConversionResult] = []
    
    def add_strategy(self, strategy: BaseConversionStrategy) -> "RedundantDataConverter":
        """
        Add a conversion strategy to the converter.
        
        Args:
            strategy: The strategy to add
            
        Returns:
            RedundantDataConverter: Self for method chaining
        """
        if not isinstance(strategy, BaseConversionStrategy):
            raise TypeError("Strategy must be an instance of BaseConversionStrategy")
        self._strategies.append(strategy)
        self._strategies.sort()
        return self
    
    def remove_strategy(self, strategy: BaseConversionStrategy) -> "RedundantDataConverter":
        """
        Remove a conversion strategy from the converter.
        
        Args:
            strategy: The strategy to remove
            
        Returns:
            RedundantDataConverter: Self for method chaining
        """
        if strategy in self._strategies:
            self._strategies.remove(strategy)
        return self
    
    def clear_strategies(self) -> "RedundantDataConverter":
        """
        Clear all conversion strategies.
        
        Returns:
            RedundantDataConverter: Self for method chaining
        """
        self._strategies.clear()
        return self
    
    def convert(self, input_value: Any, **kwargs) -> ConversionResult:
        """
        Apply all enabled strategies to the input value.
        
        Args:
            input_value: The value to convert
            **kwargs: Additional parameters passed to strategies
            
        Returns:
            ConversionResult: The final converted result
        """
        if not self._enabled:
            return ConversionResult(
                success=True,
                value=input_value,
                original=input_value,
                source_type=type(input_value).__name__,
                target_type=type(input_value).__name__,
                conversion_type=ConversionType.STR,
                steps=[],
                metadata={"message": "Converter is disabled"}
            )
        
        current_value = input_value
        all_steps = []
        metadata = {"input_type": type(input_value).__name__}
        
        for strategy in self._strategies:
            if not strategy.enabled or not strategy.can_convert(current_value):
                continue
            
            result = strategy.convert(current_value, **kwargs)
            
            if result.success:
                current_value = result.value
                all_steps.extend(result.steps)
                metadata.update(result.metadata)
            else:
                self._conversion_log.append(result)
                return result
        
        final_result = ConversionResult(
            success=True,
            value=current_value,
            original=input_value,
            source_type=type(input_value).__name__,
            target_type=type(current_value).__name__,
            conversion_type=self._strategies[0].conversion_type if self._strategies else ConversionType.STR,
            steps=all_steps,
            metadata=metadata
        )
        
        self._conversion_log.append(final_result)
        return final_result
    
    def convert_batch(
        self,
        input_values: List[Any],
        **kwargs
    ) -> List[ConversionResult]:
        """
        Convert multiple values in batch.
        
        Args:
            input_values: List of values to convert
            **kwargs: Additional parameters passed to strategies
            
        Returns:
            List[ConversionResult]: List of converted results
        """
        return [self.convert(v, **kwargs) for v in input_values]
    
    def get_conversion_log(self) -> List[ConversionResult]:
        """
        Get the log of all conversions performed.
        
        Returns:
            List[ConversionResult]: List of conversion results
        """
        return self._conversion_log.copy()
    
    def clear_conversion_log(self) -> None:
        """Clear the conversion log."""
        self._conversion_log.clear()
    
    def enable(self) -> "RedundantDataConverter":
        """
        Enable the converter.
        
        Returns:
            RedundantDataConverter: Self for method chaining
        """
        self._enabled = True
        return self
    
    def disable(self) -> "RedundantDataConverter":
        """
        Disable the converter.
        
        Returns:
            RedundantDataConverter: Self for method chaining
        """
        self._enabled = False
        return self
    
    def is_enabled(self) -> bool:
        """
        Check if the converter is enabled.
        
        Returns:
            bool: True if enabled
        """
        return self._enabled
    
    def __len__(self) -> int:
        """Return the number of registered strategies."""
        return len(self._strategies)
    
    def __repr__(self) -> str:
        """Return a string representation of the converter."""
        enabled_strategies = sum(1 for s in self._strategies if s.enabled)
        return (f"RedundantDataConverter(strategies={len(self._strategies)}, "
                f"enabled={enabled_strategies}, converter_enabled={self._enabled})")


# Type aliases for backward compatibility
ConversionStrategy = BaseConversionStrategy
