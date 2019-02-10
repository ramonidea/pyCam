from utils import *
import time
from multiprocessing import Pool
from socket import *

def transmit_image(port,hostAddr, data):
    print(port)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((hostAddr, port))
    s.sendto(data, (hostAddr, port))
    s.close()

def prepare_data(data):
    return str(data[2]) + "f" + data[0]

if __name__ == "__main__":
    camera = VisionSensor(mock=True)
    camera.start_camera()
    camera.create_streams()
    camera.sync()
    while True:
        rawdata = [prepare_data(camera.get_compressed_frame()) for x in range(30)]

        p = Pool(processes=30)
        ret = [p.apply_async(transmit_image, (5000 + x, '192.168.177', rawdata[x])) for x in range(10)]
        p.close()
        p.join()

        #cv2.imshow('image',cv2.imdecode(np.frombuffer(color, np.uint8), -1))
        ##if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    #cv2.destroyAllWindows()
