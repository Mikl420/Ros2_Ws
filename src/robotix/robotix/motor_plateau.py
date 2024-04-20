import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import struct
import math
from std_msgs.msg import String
#import sensor_msgs.point_cloud2 as pc2

class SimplePointCloudSubscriber(Node):
    def __init__(self):
        super().__init__('simple_pc2_subscriber')
        self.msg = String()
        self.publisher = self.create_publisher(String, "/robotix/stop", 10)
        self.subscription = self.create_subscription(
            PointCloud2,
            '/tof_1',
            self.listener_callback,
            10)

        self.subscription2 = self.create_subscription(
            PointCloud2,
            '/tof_2',
            self.listener_callback_2,
            10)

        self.subscription3 = self.create_subscription(
            PointCloud2,
            '/tof_3',
            self.listener_callback_3,
            10)

        self.subscription4 = self.create_subscription(
            PointCloud2,
            '/tof_4',
            self.listener_callback_4,
            10)
        
    def my_publish(self):
        self.msg.data = ('Z')
        print(self.msg.data)
        self.publisher.publish(self.msg)

    def listener_callback(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("111111111111 New point cloud data received: 1111111111111111111111111111")
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.15:
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.my_publish()
  
    def listener_callback_2(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("222222222222222 New point cloud data received:      2222222222222")
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.15:
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.my_publish()

    def listener_callback_3(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("3333333333333333 New point cloud data received:   3333333333333333333333333333333")
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.15:
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.my_publish()

    def listener_callback_4(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("44444444444444444 New point cloud data received: 4444444444444444")
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.15:
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.my_publish()
    
    def read_points(self, cloud, field_names=None, skip_nans=False, uvs=[]):
        fmt = self._get_struct_fmt(cloud.is_bigendian, cloud.fields, field_names)
        width, height, point_step, row_step = cloud.width, cloud.height, cloud.point_step, cloud.row_step
        unpack_from = struct.Struct(fmt).unpack_from

        data = cloud.data
        print("=========================== DEBUT ====================")
        for v in range(height):
            offset = v * row_step
            for u in range(width):
                p = unpack_from(data, offset)
                has_nan = skip_nans and any(math.isnan(x) for x in p)  # Properly use math.isnan() to check for NaNs
                if not has_nan:  # Correct syntax here
                    yield p
                offset += point_step
        print("============================FIN========================")
    
    def _get_struct_fmt(self, is_bigendian, fields, field_names=None):
        fmt = '>' if is_bigendian else '<'

        offset = 0
        for field in sorted(fields, key=lambda f: f.offset):
            if field_names is None or field.name in field_names:
                if offset < field.offset:
                    fmt += str(field.offset - offset) + 'x'
                if field.datatype == PointField.INT8:
                    fmt += 'b'
                elif field.datatype == PointField.UINT8:
                    fmt += 'B'
                elif field.datatype == PointField.INT16:
                    fmt += 'h'
                elif field.datatype == PointField.UINT16:
                    fmt += 'H'
                elif field.datatype == PointField.INT32:
                    fmt += 'i'
                elif field.datatype == PointField.UINT32:
                    fmt += 'I'
                elif field.datatype == PointField.FLOAT32:
                    fmt += 'f'
                elif field.datatype == PointField.FLOAT64:
                    fmt += 'd'
                offset = field.offset + struct.calcsize(fmt[-1])
        return fmt

def main(args=None):
    rclpy.init(args=args)
    simple_pc2_subscriber = SimplePointCloudSubscriber()
    rclpy.spin(simple_pc2_subscriber)
    # Cleanup
    simple_pc2_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

