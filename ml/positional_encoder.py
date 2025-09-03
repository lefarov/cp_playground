import numpy as np

def pos_encoding(position: int, d_model: int):
	# Your code here

    # resulting memory
    encoding = np.empty([position, d_model], dtype=np.float16)
    
    k = np.repeat(np.arange(position)[..., np.newaxis], d_model // 2, axis=1)
    i = np.repeat(np.arange(d_model // 2)[np.newaxis, ...], position, axis=0)

    denom = np.power(10_000, 2 * i / d_model)
    _sin = np.sin(k / denom)
    _cos = np.cos(k / denom)

    even_inds = np.arange(0, d_model, 2)
    odd_inds = np.arange(1, d_model, 2)

    encoding[..., even_inds] = _sin
    encoding[..., odd_inds] = _cos

    return encoding


if __name__ == "__main__":
	pos_encoding(2, 8)
    # [ 0.,0.,0.,0.,1.,1.,1.,1.,]
    # [ 0.8413,0.0998,0.01,0.001,0.5405,0.995,1.,1.]