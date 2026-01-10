"""
Custom Math Engine Module
==========================

This module provides an over-engineered mathematical computation engine
that implements the Strategy Pattern for various mathematical operations.

Key Features:
    - Abstract base classes for extensibility
    - Support for arithmetic, statistical, and geometric operations
    - Comprehensive type annotations with generic types
    - Detailed docstrings
    - Result validation and error handling
"""

from abc import ABC, abstractmethod
from typing import List, Union, Optional, Callable, TypeVar, Generic, Any
from dataclasses import dataclass, field
from enum import Enum
import math
import statistics
from decimal import Decimal, getcontext


# Set high precision for decimal calculations
getcontext().prec = 28


T = TypeVar("T")
NumericType = Union[int, float, Decimal]


class OperationType(Enum):
    """Enumeration of supported mathematical operation types."""
    # Arithmetic
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"
    ROOT = "root"
    MODULO = "modulo"
    
    # Statistical
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    VARIANCE = "variance"
    STD_DEV = "std_dev"
    
    # Geometric
    DISTANCE = "distance"
    ANGLE = "angle"
    AREA = "area"
    PERIMETER = "perimeter"
    VOLUME = "volume"


@dataclass
class MathResult:
    """
    A data class representing the result of a mathematical operation.
    
    Attributes:
        success: Boolean indicating whether the operation succeeded
        value: The computed result value
        operation: The type of operation performed
        operands: The operands used in the calculation
        precision: The precision of the result (number of decimal places)
        error: Error message if the operation failed
        metadata: Additional metadata about the computation
    """
    success: bool
    value: Any
    operation: OperationType
    operands: List[NumericType]
    precision: int = 6
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """
        Convert the result to a dictionary representation.
        
        Returns:
            dict: Dictionary representation of the result
        """
        return {
            "success": self.success,
            "value": float(self.value) if isinstance(self.value, (int, float, Decimal)) else 
                      [float(v) for v in self.value] if isinstance(self.value, list) else str(self.value),
            "operation": self.operation.value,
            "operands": [float(o) if isinstance(o, (int, float, Decimal)) else str(o) for o in self.operands],
            "precision": self.precision,
            "error": self.error,
            "metadata": self.metadata
        }
    
    def __repr__(self) -> str:
        """Return a string representation of the result."""
        if self.success:
            return f"MathResult(operation={self.operation.value}, value={self.value})"
        return f"MathResult(operation={self.operation.value}, error={self.error})"


class BaseMathematicalOperation(ABC, Generic[T]):
    """
    Abstract base class defining the contract for mathematical operations.
    
    This class implements the Strategy Pattern, allowing different
    mathematical operations to be interchangeable.
    
    Attributes:
        operation_type: The type of mathematical operation
        precision: Decimal precision for calculations
        enabled: Whether this operation is currently enabled
    """
    
    def __init__(
        self,
        operation_type: OperationType,
        precision: int = 6,
        enabled: bool = True
    ):
        """
        Initialize the mathematical operation.
        
        Args:
            operation_type: The type of operation
            precision: Decimal precision for calculations
            enabled: Whether the operation is enabled
        """
        self.operation_type = operation_type
        self.precision = precision
        self.enabled = enabled
    
    @abstractmethod
    def compute(self, *args: NumericType) -> MathResult:
        """
        Perform the mathematical computation.
        
        Args:
            *args: Variable number of numeric operands
            
        Returns:
            MathResult: The result of the computation
        """
        pass
    
    @abstractmethod
    def validate_operands(self, *args: NumericType) -> bool:
        """
        Validate that the operands are suitable for this operation.
        
        Args:
            *args: Variable number of numeric operands
            
        Returns:
            bool: True if operands are valid
        """
        pass
    
    def _to_decimal(self, value: NumericType) -> Decimal:
        """
        Convert a value to Decimal for precise calculations.
        
        Args:
            value: The value to convert
            
        Returns:
            Decimal: The decimal representation
        """
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))
    
    def _round_result(self, value: NumericType) -> Union[int, float]:
        """
        Round the result to the specified precision.
        
        Args:
            value: The value to round
            
        Returns:
            Union[int, float]: The rounded value
        """
        if isinstance(value, Decimal):
            return round(float(value), self.precision)
        if isinstance(value, float):
            return round(value, self.precision)
        return value
    
    def __repr__(self) -> str:
        """Return a string representation of the operation."""
        return f"{self.__class__.__name__}(type={self.operation_type.value}, enabled={self.enabled})"


class ArithmeticOperation(BaseMathematicalOperation):
    """
    A strategy for performing basic arithmetic operations.
    
    Supports addition, subtraction, multiplication, division,
    exponentiation, root extraction, and modulo operations.
    """
    
    def __init__(
        self,
        operation_type: Union[OperationType, str],
        precision: int = 6,
        enabled: bool = True
    ):
        """
        Initialize the arithmetic operation.
        
        Args:
            operation_type: The type of arithmetic operation
            precision: Decimal precision for calculations
            enabled: Whether the operation is enabled
        """
        if isinstance(operation_type, str):
            operation_type = OperationType(operation_type.lower())
        
        # Validate that it's an arithmetic operation
        arithmetic_ops = {
            OperationType.ADD, OperationType.SUBTRACT, OperationType.MULTIPLY,
            OperationType.DIVIDE, OperationType.POWER, OperationType.ROOT,
            OperationType.MODULO
        }
        
        if operation_type not in arithmetic_ops:
            raise ValueError(f"Invalid arithmetic operation type: {operation_type}")
        
        super().__init__(operation_type, precision, enabled)
    
    def compute(self, *args: NumericType) -> MathResult:
        """
        Perform the arithmetic computation.
        
        Args:
            *args: Variable number of numeric operands (1-2 operands)
            
        Returns:
            MathResult: The result of the computation
        """
        operands = list(args)
        
        if not self.validate_operands(*args):
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error=f"Invalid operands for {self.operation_type.value}"
            )
        
        try:
            if self.operation_type == OperationType.ADD:
                result = self._add(operands)
            elif self.operation_type == OperationType.SUBTRACT:
                result = self._subtract(operands)
            elif self.operation_type == OperationType.MULTIPLY:
                result = self._multiply(operands)
            elif self.operation_type == OperationType.DIVIDE:
                result = self._divide(operands)
            elif self.operation_type == OperationType.POWER:
                result = self._power(operands)
            elif self.operation_type == OperationType.ROOT:
                result = self._root(operands)
            elif self.operation_type == OperationType.MODULO:
                result = self._modulo(operands)
            else:
                raise ValueError(f"Unsupported operation: {self.operation_type}")
            
            return MathResult(
                success=True,
                value=result,
                operation=self.operation_type,
                operands=operands,
                precision=self.precision,
                metadata={"computation_method": "decimal"}
            )
        except ZeroDivisionError:
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error="Division by zero"
            )
        except Exception as e:
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error=str(e)
            )
    
    def validate_operands(self, *args: NumericType) -> bool:
        """
        Validate that the operands are suitable for this operation.
        
        Args:
            *args: Variable number of numeric operands
            
        Returns:
            bool: True if operands are valid
        """
        if not args:
            return False
        
        for arg in args:
            if not isinstance(arg, (int, float, Decimal)):
                return False
        
        return True
    
    def _add(self, operands: List[NumericType]) -> float:
        """Perform addition."""
        result = Decimal(0)
        for operand in operands:
            result += self._to_decimal(operand)
        return self._round_result(result)
    
    def _subtract(self, operands: List[NumericType]) -> float:
        """Perform subtraction."""
        if len(operands) < 2:
            raise ValueError("Subtraction requires at least 2 operands")
        result = self._to_decimal(operands[0])
        for operand in operands[1:]:
            result -= self._to_decimal(operand)
        return self._round_result(result)
    
    def _multiply(self, operands: List[NumericType]) -> float:
        """Perform multiplication."""
        result = Decimal(1)
        for operand in operands:
            result *= self._to_decimal(operand)
        return self._round_result(result)
    
    def _divide(self, operands: List[NumericType]) -> float:
        """Perform division."""
        if len(operands) < 2:
            raise ValueError("Division requires at least 2 operands")
        result = self._to_decimal(operands[0])
        for operand in operands[1:]:
            divisor = self._to_decimal(operand)
            if divisor == 0:
                raise ZeroDivisionError()
            result /= divisor
        return self._round_result(result)
    
    def _power(self, operands: List[NumericType]) -> float:
        """Perform exponentiation."""
        if len(operands) != 2:
            raise ValueError("Power operation requires exactly 2 operands")
        base = float(operands[0])
        exponent = float(operands[1])
        result = base ** exponent
        return round(result, self.precision)
    
    def _root(self, operands: List[NumericType]) -> float:
        """Perform root extraction."""
        if len(operands) != 2:
            raise ValueError("Root operation requires exactly 2 operands")
        radicand = float(operands[0])
        degree = float(operands[1])
        if degree == 0:
            raise ValueError("Root degree cannot be zero")
        if radicand < 0 and int(degree) % 2 == 0:
            raise ValueError("Even root of negative number is not real")
        result = radicand ** (1.0 / degree)
        return round(result, self.precision)
    
    def _modulo(self, operands: List[NumericType]) -> float:
        """Perform modulo operation."""
        if len(operands) != 2:
            raise ValueError("Modulo operation requires exactly 2 operands")
        dividend = self._to_decimal(operands[0])
        divisor = self._to_decimal(operands[1])
        if divisor == 0:
            raise ZeroDivisionError()
        result = dividend % divisor
        return self._round_result(result)


class StatisticalOperation(BaseMathematicalOperation):
    """
    A strategy for performing statistical calculations.
    
    Supports mean, median, mode, variance, and standard deviation calculations.
    """
    
    def __init__(
        self,
        operation_type: Union[OperationType, str],
        precision: int = 6,
        enabled: bool = True
    ):
        """
        Initialize the statistical operation.
        
        Args:
            operation_type: The type of statistical operation
            precision: Decimal precision for calculations
            enabled: Whether the operation is enabled
        """
        if isinstance(operation_type, str):
            operation_type = OperationType(operation_type.lower())
        
        # Validate that it's a statistical operation
        statistical_ops = {
            OperationType.MEAN, OperationType.MEDIAN, OperationType.MODE,
            OperationType.VARIANCE, OperationType.STD_DEV
        }
        
        if operation_type not in statistical_ops:
            raise ValueError(f"Invalid statistical operation type: {operation_type}")
        
        super().__init__(operation_type, precision, enabled)
    
    def compute(self, *args: NumericType) -> MathResult:
        """
        Perform the statistical computation.
        
        Args:
            *args: Variable number of numeric operands (data points)
            
        Returns:
            MathResult: The result of the computation
        """
        operands = list(args)
        
        if not self.validate_operands(*args):
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error=f"Invalid operands for {self.operation_type.value}"
            )
        
        try:
            if self.operation_type == OperationType.MEAN:
                result = self._mean(operands)
            elif self.operation_type == OperationType.MEDIAN:
                result = self._median(operands)
            elif self.operation_type == OperationType.MODE:
                result = self._mode(operands)
            elif self.operation_type == OperationType.VARIANCE:
                result = self._variance(operands)
            elif self.operation_type == OperationType.STD_DEV:
                result = self._std_dev(operands)
            else:
                raise ValueError(f"Unsupported operation: {self.operation_type}")
            
            return MathResult(
                success=True,
                value=result,
                operation=self.operation_type,
                operands=operands,
                precision=self.precision,
                metadata={
                    "sample_size": len(operands),
                    "computation_method": "statistics_module"
                }
            )
        except Exception as e:
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error=str(e)
            )
    
    def validate_operands(self, *args: NumericType) -> bool:
        """
        Validate that the operands are suitable for this operation.
        
        Args:
            *args: Variable number of numeric operands
            
        Returns:
            bool: True if operands are valid
        """
        if not args or len(args) < 1:
            return False
        
        for arg in args:
            if not isinstance(arg, (int, float, Decimal)):
                return False
        
        return True
    
    def _mean(self, data: List[NumericType]) -> float:
        """Calculate the arithmetic mean."""
        float_data = [float(d) for d in data]
        return round(statistics.mean(float_data), self.precision)
    
    def _median(self, data: List[NumericType]) -> float:
        """Calculate the median."""
        float_data = [float(d) for d in data]
        return round(statistics.median(float_data), self.precision)
    
    def _mode(self, data: List[NumericType]) -> Union[float, List[float]]:
        """Calculate the mode (most common value)."""
        float_data = [float(d) for d in data]
        try:
            modes = statistics.multimode(float_data)
            if len(modes) == 1:
                return round(modes[0], self.precision)
            return [round(m, self.precision) for m in modes]
        except statistics.StatisticsError:
            return 0.0
    
    def _variance(self, data: List[NumericType]) -> float:
        """Calculate the population variance."""
        if len(data) < 2:
            raise ValueError("Variance requires at least 2 data points")
        float_data = [float(d) for d in data]
        return round(statistics.pvariance(float_data), self.precision)
    
    def _std_dev(self, data: List[NumericType]) -> float:
        """Calculate the population standard deviation."""
        if len(data) < 2:
            raise ValueError("Standard deviation requires at least 2 data points")
        float_data = [float(d) for d in data]
        return round(statistics.pstdev(float_data), self.precision)


class GeometricOperation(BaseMathematicalOperation):
    """
    A strategy for performing geometric calculations.
    
    Supports distance, angle, area, perimeter, and volume calculations.
    """
    
    def __init__(
        self,
        operation_type: Union[OperationType, str],
        precision: int = 6,
        enabled: bool = True
    ):
        """
        Initialize the geometric operation.
        
        Args:
            operation_type: The type of geometric operation
            precision: Decimal precision for calculations
            enabled: Whether the operation is enabled
        """
        if isinstance(operation_type, str):
            operation_type = OperationType(operation_type.lower())
        
        # Validate that it's a geometric operation
        geometric_ops = {
            OperationType.DISTANCE, OperationType.ANGLE,
            OperationType.AREA, OperationType.PERIMETER, OperationType.VOLUME
        }
        
        if operation_type not in geometric_ops:
            raise ValueError(f"Invalid geometric operation type: {operation_type}")
        
        super().__init__(operation_type, precision, enabled)
    
    def compute(self, *args: NumericType) -> MathResult:
        """
        Perform the geometric computation.
        
        Args:
            *args: Variable number of numeric operands (coordinates, dimensions, etc.)
            
        Returns:
            MathResult: The result of the computation
        """
        operands = list(args)
        
        if not self.validate_operands(*args):
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error=f"Invalid operands for {self.operation_type.value}"
            )
        
        try:
            if self.operation_type == OperationType.DISTANCE:
                result = self._distance(operands)
            elif self.operation_type == OperationType.ANGLE:
                result = self._angle(operands)
            elif self.operation_type == OperationType.AREA:
                result = self._area(operands)
            elif self.operation_type == OperationType.PERIMETER:
                result = self._perimeter(operands)
            elif self.operation_type == OperationType.VOLUME:
                result = self._volume(operands)
            else:
                raise ValueError(f"Unsupported operation: {self.operation_type}")
            
            return MathResult(
                success=True,
                value=result,
                operation=self.operation_type,
                operands=operands,
                precision=self.precision,
                metadata={"computation_method": "geometric_formula"}
            )
        except Exception as e:
            return MathResult(
                success=False,
                value=0,
                operation=self.operation_type,
                operands=operands,
                error=str(e)
            )
    
    def validate_operands(self, *args: NumericType) -> bool:
        """
        Validate that the operands are suitable for this operation.
        
        Args:
            *args: Variable number of numeric operands
            
        Returns:
            bool: True if operands are valid
        """
        if not args:
            return False
        
        for arg in args:
            if not isinstance(arg, (int, float, Decimal)):
                return False
        
        return True
    
    def _distance(self, operands: List[NumericType]) -> float:
        """
        Calculate Euclidean distance between two 2D points.
        
        Args:
            operands: [x1, y1, x2, y2]
        """
        if len(operands) != 4:
            raise ValueError("Distance calculation requires exactly 4 coordinates (x1, y1, x2, y2)")
        x1, y1, x2, y2 = [float(o) for o in operands]
        return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), self.precision)
    
    def _angle(self, operands: List[NumericType]) -> float:
        """
        Calculate angle between two vectors in degrees.
        
        Args:
            operands: [x1, y1, x2, y2]
        """
        if len(operands) != 4:
            raise ValueError("Angle calculation requires exactly 4 coordinates")
        x1, y1, x2, y2 = [float(o) for o in operands]
        
        dot_product = x1 * x2 + y1 * y2
        magnitude1 = math.sqrt(x1**2 + y1**2)
        magnitude2 = math.sqrt(x2**2 + y2**2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            raise ValueError("Zero vector detected")
        
        cos_angle = dot_product / (magnitude1 * magnitude2)
        cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to [-1, 1]
        angle_rad = math.acos(cos_angle)
        return round(math.degrees(angle_rad), self.precision)
    
    def _area(self, operands: List[NumericType]) -> float:
        """
        Calculate area of a rectangle.
        
        Args:
            operands: [width, height]
        """
        if len(operands) != 2:
            raise ValueError("Rectangle area calculation requires exactly 2 dimensions")
        width, height = [float(o) for o in operands]
        if width < 0 or height < 0:
            raise ValueError("Dimensions must be non-negative")
        return round(width * height, self.precision)
    
    def _perimeter(self, operands: List[NumericType]) -> float:
        """
        Calculate perimeter of a rectangle.
        
        Args:
            operands: [width, height]
        """
        if len(operands) != 2:
            raise ValueError("Rectangle perimeter calculation requires exactly 2 dimensions")
        width, height = [float(o) for o in operands]
        if width < 0 or height < 0:
            raise ValueError("Dimensions must be non-negative")
        return round(2 * (width + height), self.precision)
    
    def _volume(self, operands: List[NumericType]) -> float:
        """
        Calculate volume of a rectangular prism.
        
        Args:
            operands: [length, width, height]
        """
        if len(operands) != 3:
            raise ValueError("Prism volume calculation requires exactly 3 dimensions")
        length, width, height = [float(o) for o in operands]
        if length < 0 or width < 0 or height < 0:
            raise ValueError("Dimensions must be non-negative")
        return round(length * width * height, self.precision)


class CustomMathEngine:
    """
    An advanced mathematical computation engine that orchestrates multiple
    mathematical operations using the Strategy Pattern.
    
    Example:
        >>> engine = CustomMathEngine()
        >>> engine.register_operation(ArithmeticOperation(OperationType.ADD))
        >>> engine.register_operation(StatisticalOperation(OperationType.MEAN))
        >>> result = engine.compute(OperationType.ADD, 5, 3)
        >>> print(result.value)
        8.0
    """
    
    def __init__(self, default_precision: int = 6):
        """
        Initialize the math engine.
        
        Args:
            default_precision: Default precision for calculations
        """
        self._operations: dict[OperationType, BaseMathematicalOperation] = {}
        self._default_precision = default_precision
        self._computation_log: List[MathResult] = []
        self._enabled: bool = True
    
    def register_operation(
        self,
        operation: BaseMathematicalOperation
    ) -> "CustomMathEngine":
        """
        Register a mathematical operation with the engine.
        
        Args:
            operation: The operation to register
            
        Returns:
            CustomMathEngine: Self for method chaining
        """
        if not isinstance(operation, BaseMathematicalOperation):
            raise TypeError("Operation must be an instance of BaseMathematicalOperation")
        self._operations[operation.operation_type] = operation
        return self
    
    def unregister_operation(
        self,
        operation_type: OperationType
    ) -> "CustomMathEngine":
        """
        Unregister a mathematical operation from the engine.
        
        Args:
            operation_type: The type of operation to unregister
            
        Returns:
            CustomMathEngine: Self for method chaining
        """
        if operation_type in self._operations:
            del self._operations[operation_type]
        return self
    
    def get_registered_operations(self) -> List[OperationType]:
        """
        Get a list of registered operation types.
        
        Returns:
            List[OperationType]: List of registered operation types
        """
        return list(self._operations.keys())
    
    def compute(
        self,
        operation_type: Union[OperationType, str],
        *args: NumericType
    ) -> MathResult:
        """
        Perform a mathematical computation using the specified operation.
        
        Args:
            operation_type: The type of operation to perform
            *args: Variable number of numeric operands
            
        Returns:
            MathResult: The result of the computation
        """
        if not self._enabled:
            return MathResult(
                success=False,
                value=0,
                operation=OperationType(operation_type) if isinstance(operation_type, str) else operation_type,
                operands=list(args),
                error="Math engine is disabled"
            )
        
        if isinstance(operation_type, str):
            try:
                operation_type = OperationType(operation_type.lower())
            except ValueError:
                return MathResult(
                    success=False,
                    value=0,
                    operation=OperationType.ADD,
                    operands=list(args),
                    error=f"Unknown operation type: {operation_type}"
                )
        
        if operation_type not in self._operations:
            return MathResult(
                success=False,
                value=0,
                operation=operation_type,
                operands=list(args),
                error=f"Operation {operation_type.value} not registered"
            )
        
        operation = self._operations[operation_type]
        
        if not operation.enabled:
            return MathResult(
                success=False,
                value=0,
                operation=operation_type,
                operands=list(args),
                error=f"Operation {operation_type.value} is disabled"
            )
        
        result = operation.compute(*args)
        self._computation_log.append(result)
        return result
    
    def compute_batch(
        self,
        operation_type: Union[OperationType, str],
        operand_sets: List[List[NumericType]]
    ) -> List[MathResult]:
        """
        Perform multiple computations of the same type.
        
        Args:
            operation_type: The type of operation to perform
            operand_sets: List of operand sets for each computation
            
        Returns:
            List[MathResult]: List of computation results
        """
        return [self.compute(operation_type, *operands) for operands in operand_sets]
    
    def enable_operation(self, operation_type: OperationType) -> "CustomMathEngine":
        """
        Enable a specific operation.
        
        Args:
            operation_type: The operation type to enable
            
        Returns:
            CustomMathEngine: Self for method chaining
        """
        if operation_type in self._operations:
            self._operations[operation_type].enabled = True
        return self
    
    def disable_operation(self, operation_type: OperationType) -> "CustomMathEngine":
        """
        Disable a specific operation.
        
        Args:
            operation_type: The operation type to disable
            
        Returns:
            CustomMathEngine: Self for method chaining
        """
        if operation_type in self._operations:
            self._operations[operation_type].enabled = False
        return self
    
    def get_computation_log(self) -> List[MathResult]:
        """
        Get the log of all computations performed.
        
        Returns:
            List[MathResult]: List of computation results
        """
        return self._computation_log.copy()
    
    def clear_computation_log(self) -> None:
        """Clear the computation log."""
        self._computation_log.clear()
    
    def enable(self) -> "CustomMathEngine":
        """
        Enable the math engine.
        
        Returns:
            CustomMathEngine: Self for method chaining
        """
        self._enabled = True
        return self
    
    def disable(self) -> "CustomMathEngine":
        """
        Disable the math engine.
        
        Returns:
            CustomMathEngine: Self for method chaining
        """
        self._enabled = False
        return self
    
    def is_enabled(self) -> bool:
        """
        Check if the math engine is enabled.
        
        Returns:
            bool: True if enabled
        """
        return self._enabled
    
    def __len__(self) -> int:
        """Return the number of registered operations."""
        return len(self._operations)
    
    def __repr__(self) -> str:
        """Return a string representation of the engine."""
        enabled_ops = sum(1 for op in self._operations.values() if op.enabled)
        return (f"CustomMathEngine(operations={len(self._operations)}, "
                f"enabled={enabled_ops}, engine_enabled={self._enabled})")


# Type aliases for backward compatibility
MathematicalOperation = BaseMathematicalOperation
