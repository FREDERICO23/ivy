# global
import tensorflow as tf
from typing import Union, Optional

# local
import ivy


def argsort(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    direction = "DESCENDING" if descending else "ASCENDING"
    x = tf.convert_to_tensor(x)
    is_bool = x.dtype.is_bool
    if is_bool:
        x = tf.cast(x, tf.int32)
    ret = tf.argsort(x, axis=axis, direction=direction, stable=stable)
    return tf.cast(ret, dtype=tf.int64)


def sort(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    # TODO: handle stable sort when it's supported in tensorflow
    # currently it supports only quicksort (unstable)
    direction = "DESCENDING" if descending else "ASCENDING"
    x = tf.convert_to_tensor(x)
    is_bool = x.dtype.is_bool
    if is_bool:
        x = tf.cast(x, tf.int32)
    ret = tf.sort(x, axis=axis, direction=direction)
    if is_bool:
        ret = tf.cast(ret, dtype=tf.bool)
    return ret


def searchsorted(
    x: Union[tf.Tensor, tf.Variable],
    v: Union[tf.Tensor, tf.Variable],
    /,
    *,
    side="left",
    sorter=None,
    ret_dtype=tf.int64,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    assert ivy.is_int_dtype(ret_dtype), ValueError(
        "only Integer data types are supported for ret_dtype."
    )
    is_supported_int_ret_dtype = ret_dtype in [tf.int32, tf.int64]
    if sorter is not None:
        assert ivy.is_int_dtype(sorter.dtype) and not ivy.is_uint_dtype(
            sorter.dtype
        ), TypeError(
            f"Only signed integer data type for sorter is allowed, got {sorter.dtype}."
        )
        if sorter.dtype not in [tf.int32, tf.int64]:
            sorter = tf.cast(sorter, tf.int32)
        if x.ndim == 1:
            x = tf.gather(x, sorter)
        else:
            x = tf.gather(x, sorter, batch_dims=-1)
    if x.ndim == 1 and v.ndim != 1:
        out_shape = v.shape
        v = tf.reshape(v, (1, -1))  # Leading dims must be the same
        if is_supported_int_ret_dtype:
            return tf.reshape(
                tf.searchsorted(x, v, side=side, out_type=ret_dtype), out_shape
            )
        else:
            return tf.cast(
                tf.reshape(tf.searchsorted(x, v, side=side), out_shape), ret_dtype
            )
    if is_supported_int_ret_dtype:
        return tf.searchsorted(x, v, side=side, out_type=ret_dtype)
    return tf.cast(tf.searchsorted(x, v, side=side), ret_dtype)
