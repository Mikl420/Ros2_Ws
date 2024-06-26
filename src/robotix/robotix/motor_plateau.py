import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import struct
import math
from std_msgs.msg import String
import RPi.GPIO as GPIO

class SimplePointCloudSubscriber(Node):
    def __init__(self):
        super().__init__('simple_pc2_subscriber')
        self.pin = 24  # Change to your GPIO pin number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)  #,pull_up_down=GPIO.PUD_UP)
        self.msg = String()
        self.capteur1 = False
        self.capteur2 = False
        self.capteur3 = False
        self.capteur4 = False
        self.cpt_capteur1 = 0
        self.cpt_capteur2 = 0
        self.cpt_capteur3 = 0
        self.cpt_capteur4 = 0
        #self.publisher = self.create_publisher(String, "/robotix/stop", 10)
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
        
    #def my_publish(self, stop):
        #self.msg.data = ('Z')
        #print(self.msg.data)
        #self.publisher.publish(self.msg)
        

    def listener_callback(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("111111111111 New point cloud data received: 1111111111111111111111111111")
        self.cpt_capteur1 = 0
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.3 :
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.cpt_capteur1 = self.cpt_capteur1 + 1
        if self.cpt_capteur1 > 1:
            self.capteur1 = False
        else:
            self.capteur1 = True
        self.interrupt_or_not()
        
  
    def listener_callback_2(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("222222222222222 New point cloud data received:      2222222222222")
        self.cpt_capteur2 = 0
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.3 :
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.cpt_capteur2 = self.cpt_capteur2 + 1
        if self.cpt_capteur2 > 1:
            self.capteur2 = False
        else:
            self.capteur2 = True
        self.interrupt_or_not()

    def listener_callback_3(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        print("3333333333333333 New point cloud data received:   3333333333333333333333333333333")
        self.cpt_capteur3 = 0
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.3 :
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.cpt_capteur3 = self.cpt_capteur3 + 1
        if self.cpt_capteur3 > 1:
            self.capteur3 = False
        else:
            self.capteur3 = True
        self.interrupt_or_not()

    def listener_callback_4(self, msg):
        # Parse the point cloud data
        assert isinstance(msg, PointCloud2)
        points = self.read_points(msg)
        self.cpt_capteur4 = 0
        print("44444444444444444 New point cloud data received: 4444444444444444")
        for point in points:
            if  point[0] < 0.01 and point[0] > -0.01 and point[2] > 0.1 and point[2] < 0.3 :
                print(f"x: {point[0]:.2f}, y: {point[1]:.2f}, z: {point[2]:.2f}")
                self.cpt_capteur4 = self.cpt_capteur4 + 1
        if self.cpt_capteur4 > 1:
            self.capteur4 = False
        else:
            self.capteur4 = True
        self.interrupt_or_not()

    def interrupt_or_not(self):
        if not self.capteur1 or not self.capteur2 or not self.capteur3 or not self.capteur4:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)
    
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

