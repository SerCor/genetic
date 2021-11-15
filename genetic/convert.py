'Implementation of the functions for transform numeric variables to bits'

def bits2int(bits: str, low: int) -> int:
    return low + int(bits, 2)
    

def int2bits(ivalue: int, low: int, n_bits: int) -> str:
    if n_bits <= 0:
        raise ValueError(f'n_bits must to be a positive integer value, but is {n_bits}')
    
    relative_value = ivalue - low
    return f'{relative_value:0{n_bits}b}'


def bits2float(bits: str, low: float, high: float) -> float:
    n_bits = len(bits)
    ipartition = low + int(bits, base=2)
    partition_size = (high - low) / (2 ** n_bits)
    return low + (ipartition * partition_size)


def float2bits(fvalue: float, low: float, high: float, n_bits: int) -> str:
    offset = fvalue - low
    partition_size = (high - low) / (2 ** n_bits)
    ipartition = offset // partition_size
    return int2bits(int(ipartition), 0, n_bits)
