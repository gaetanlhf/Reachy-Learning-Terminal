from reachy_sdk import ReachySDK
import time
import threading
import sys
import pickle
import traceback

if __name__ == "__main__":
    reachy = ReachySDK(host="0.0.0.0")

    carryOn = True


    def keyCapture():
        global carryOn
        input()
        carryOn = False


    jointToRecord = [
        reachy.r_arm.r_shoulder_pitch,
        reachy.r_arm.r_shoulder_roll,
        reachy.r_arm.r_arm_yaw,
        reachy.r_arm.r_elbow_pitch,
        reachy.r_arm.r_forearm_yaw,
        reachy.r_arm.r_wrist_pitch,
        reachy.r_arm.r_wrist_roll,
        reachy.r_arm.r_gripper,
        reachy.l_arm.l_shoulder_pitch,
        reachy.l_arm.l_shoulder_roll,
        reachy.l_arm.l_arm_yaw,
        reachy.l_arm.l_elbow_pitch,
        reachy.l_arm.l_forearm_yaw,
        reachy.l_arm.l_wrist_pitch,
        reachy.l_arm.l_wrist_roll,
        reachy.l_arm.l_gripper,
        reachy.head.r_antenna,
        reachy.head.l_antenna,
        reachy.head.neck_disk_top,
        reachy.head.neck_disk_middle,
        reachy.head.neck_disk_bottom,
    ]

    learning = []

    print("Welcome to the Reachy Learning Terminal")
    print("Type `help` to find out the commands")

    try:
        while True:
            carryOn = True
            reachy.turn_off("reachy")
            typed = input("> ")

            if typed == "learn":
                learning = []
                print("Start learning in 5 seconds...")
                print("You will be able to press the `Enter` key to exit the training")
                time.sleep(5)
                print("The learning process has just started")
                threading.Thread(target=keyCapture, args=(),
                                name="keyCapture", daemon=True).start()
                while carryOn:
                    currentPoint = [
                        joint.present_position for joint in jointToRecord]
                    learning.append(currentPoint)
                    time.sleep(0.01)
                print("You stopped learning")
                print("Remember, if you wish, to save the learning!")

            elif typed == "play":
                if learning == []:
                    print("Nothing to play!")
                else:
                    print("Playing...")
                    reachy.turn_on("reachy")
                    for positions in learning:
                        for joint, position in zip(jointToRecord, positions):
                            joint.goal_position = position
                        time.sleep(0.01)
                    print("Playing ended")

            elif typed == "save":
                if learning != []:
                    f = open("learn.save", "wb")
                    pickle.dump(learning, f)
                    f.close()
                    print("Learning saved!")
                else:
                    print("Nothing to save!")

            elif typed == "load":
                try:
                    f = open("learn.save", "rb")
                    learning = pickle.load(f)
                    f.close()
                    print("Learning loaded!")
                except:
                    print("No save found!")

            elif typed == "help":
                print("`learn`: teach your Reachy to move")
                print("`play`: let your Reachy replicate your movements")
                print("`save`: save the learning experience of your Reachy")
                print("`load`: load a previously saved training course")
                print("`help`: displays this help")
                print("`exit`: exits the program")

            elif typed == "exit":
                sys.exit()

            else:
                print("Unknown command")
                print("Type `help` to find out the commands")

    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as exception:
        print("An unknown error occured!")
        print("Traceback error:", exception)
        traceback.print_exc()
    finally:
        reachy.turn_off("reachy")
        sys.exit()
