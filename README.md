# deepnude4video

DeepNude Source Code for Videos

# How to use

1. Download the model

https://github.com/zhengyima/DeepNude_NoWatermark_withModel

2. Set models in the `/checkpoints` directory

3. Set video to `videos/` directory

4. Build docker machine

```
docker build -t deepnude/4videos .
```

5. Exec docker container

```
docker run --rm -it -v $PWD:/app:rw deepnude/4videos python main.py ./videos/in.mp4 ./videos/out.mp4
```

# Base repository

https://github.com/zhengyima/DeepNude_NoWatermark_withModel

# GPU Settings

in `./lib/gan.py`

```
- self.gpu_ids = []
+ self.gpu_ids = [0]
```

# FFMEPG Cheat Sheet

Clipping

```
ffmpeg -i org.mp4 -ss 249 -t 1 in.mp4
```
