
import cv2
import os

def extractor(video,save_location,skip_frames):
    """Function to bal bla bla """
    #get adress of videofile
    video_location = cv2.VideoCapture(str(video))

    try:
        #create folder to save extrected images
        if not os.path.exists(f'extracted_images/{save_location}'):
            os.makedirs(f'extracted_images/{save_location}')
    except OSError:
        print ('Could not create folder')

    #start at frame 0
    currentframe = 0
    extracted = 0
    if skip_frames:
        skip_frames = skip_frames
    else:
        skip_frames = 2

    while(True):
        # reading from frame
        #read from source and unpack into tuple
        ret,frame = video_location.read()

        #If we have a
        if ret:
            if((currentframe % skip_frames ) == 0):
                name = './extracted_images/'+save_location+'/'+'image' + str(currentframe) + '.jpg'
                print(f"Saving {name} from video:{video}")
                # write current frame to an image
                cv2.imwrite(name, frame)
                currentframe += 1
                extracted +=1
            else:
                currentframe += 1
                continue

        else:
            print(f"\nEXTRACTED {extracted} IMAGES IN TOTAL FROM {currentframe} FRAMES\n")
            break


    video_location.release()
    cv2.destroyAllWindows()
