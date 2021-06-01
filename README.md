# qr_utils ROS package

ROS nodes to:

- read the values stored by a QR code seen in a video stream
- get the transform between a QR code and the origin of a point cloud or depth image video stream (TODO)
- perform the same utilities on single images

# Getting QR-code values

Video streams in ROS are represented as a series of published images (`sensor_msgs/Image`). It would be computationally expensive to run the QR code recognizer on every single frame in the video stream. Instead, the node provides these alternative methods of interaction:

1) Always have the most recent frame stored, so that a service can query for the values within currently-visible QR codes
2) Constantly publish the currently-visible QR codes, but at a very limited rate (e.g., 1Hz)
3) Allow the user of the service to provide the image, and receive the resulting strings

One node handles all three cases:

```bash
rosrun qr_utils qr_reader_2d
```

The node will attempt to subscribe to a stream of `sensor_msgs/Image` on `/input_image`, you should be able to call the service `/qr_reader/read_environment`. The service takes `std_msgs/Empty` as its input, so there's nothing to input. This returns `std_msgs/string[]`, where each entry in the array is an individual QR code in the input image.

To make the node constantly publish QR code observations, the node will again need to be subscribed to an input image stream. With the parameter `/qr_reader/publish_hz` set to non-zero, however, readings will be published at the rate specified. With a negative Hz or a Hz exceeding that of the input, the publisher Hz will be set to the input Hz. Note, however, that this is very rarely necessary, and given the increased computational cost, it is not recommended. As with the service previously described, the output will be an array of strings.

Finally, an image can be provided which the reader will attempt to parse. This is done via the `/qr_reader/read_image` service, which takes in a `sensor_msgs/Image` and returns an array of strings. If this is your use-case and you would find it useful to turn off the `Image` subscriber that isn't being used in this use-case, it can be disabled via the `qr_reader/listen_to_image` boolean.
