#!/usr/bin/env python
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import PoseStamped

MARKERS_MAX = 100

class visualizer(object):
    def __init__(self):
        self.pub_marker = rospy.Publisher("~pose_visualizer", Marker, queue_size=1)
        self.pub_anchor = rospy.Publisher("~pose_array", MarkerArray, queue_size=1)
        self.pub_anchors = rospy.Publisher("~anchors", MarkerArray, queue_size=1)
        self.markerArray = MarkerArray()
        self.count = 0
        self.anchors = rospy.get_param("localize/anchors")
        
        self.anchorsarray = MarkerArray()
        
        for anchor in self.anchors:
            marker_msg = Marker()
            marker_msg.header.frame_id = "uwb_pose"
            marker_msg.header.stamp = rospy.Time()
            marker_msg.action = Marker.ADD
            marker_msg.type = Marker.SPHERE
            marker_msg.pose.position.x = float(anchor['px'])/1000
            marker_msg.pose.position.y = float(anchor['py'])/1000 
            marker_msg.pose.position.z = float(anchor['pz'])/1000
            print(marker_msg.pose.position.x,marker_msg.pose.position.y,marker_msg.pose.position.z)
            marker_msg.scale.x = 0.2
            marker_msg.scale.y = 0.2
            marker_msg.scale.z = 0.2

            marker_msg.color.r = 1.0
            marker_msg.color.g = 0
            marker_msg.color.b = 0
            marker_msg.color.a = 1.0

            marker_msg.lifetime = rospy.Duration()

            self.anchorsarray.markers.append(marker_msg)
        
        id = 0
        for m in self.anchorsarray.markers:
            m.id = id
            id += 1

        
        

        self.sub_pose = rospy.Subscriber("localize/local_tag_pose", PoseStamped, self.pose_cb, queue_size=1)

    def pose_cb(self, pose_msg):
        #print "pose cb"
        marker_msg = Marker()
        marker_msg.header.frame_id = "uwb_pose"
        marker_msg.header.stamp = rospy.Time()
        marker_msg.action = Marker.ADD
        marker_msg.type = Marker.SPHERE
        marker_msg.pose.position.x = pose_msg.pose.position.x
        marker_msg.pose.position.y = pose_msg.pose.position.y
        marker_msg.pose.position.z = pose_msg.pose.position.z

        marker_msg.pose.orientation.x = pose_msg.pose.orientation.x
        marker_msg.pose.orientation.y = pose_msg.pose.orientation.y
        marker_msg.pose.orientation.z = pose_msg.pose.orientation.z
        marker_msg.pose.orientation.w = pose_msg.pose.orientation.w
        marker_msg.scale.x = 0.2
        marker_msg.scale.y = 0.2
        marker_msg.scale.z = 0.2

        marker_msg.color.r = 1.0
        marker_msg.color.g = 1.0
        marker_msg.color.b = 1.0
        marker_msg.color.a = 1.0

        marker_msg.lifetime = rospy.Duration()
        self.pub_marker.publish(marker_msg)

        if (self.count > MARKERS_MAX):
            self.markerArray.markers.pop(0)

        self.markerArray.markers.append(marker_msg)

        id = 0
        for m in self.markerArray.markers:
            m.id = id
            id += 1

        self.pub_anchor.publish(self.markerArray)
        self.pub_anchors.publish(self.anchorsarray)

        self.count += 1

if __name__ == '__main__':
	rospy.init_node('pose_visualization',anonymous=False)
	node = visualizer()
	rospy.spin()
