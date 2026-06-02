"""
Ficher personnel non retravaillé
"""

from pynput import mouse
from pynput import keyboard
from dic_switch import KEY_NAME_TO_KEY, VK_TO_CHAR
import time


class Executor:
    def __init__(self):
        self.stopper_var = keyboard.Listener(on_press=self.stopper)
        self.loop = True
        self.count = 0
        self.mousse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.median = 0
        self.temp_list = []

    def reset(self, pass_list=None):
        self.stopper_var = keyboard.Listener(on_press=self.stopper)
        self.loop = True
        self.count = 0
        self.mousse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        if pass_list:
            self.temp_list = sorted(pass_list[1:])
            self.temp_list.pop(0)
            self.temp_list.sort()
            self.median = self.temp_list[(len(pass_list)-1) // 2]

    def stopper(self, key):
        if key == keyboard.Key.esc:
            print("stop")
            self.loop = False

    def e_mouse(self, action, pause=None):
        if pause:
            time.sleep(pause)
        self.mousse.position = action[1]
        if action[0] == 'click':
            if action[2] == 'left':
                self.mousse.click(mouse.Button.left, 1)
            else:
                self.mousse.click(mouse.Button.right, 1)
        elif action[0] == 'scroll':
            self.mousse.scroll(action[2][1], action[2][0])

    def e_keyboard(self, action, pause=None):
        if pause:
            time.sleep(pause)
        else:
            time.sleep(0.01)
        if action[0] == 'press':
            if action[1] == 'char':
                self.keyboard.press(action[2])
            else:
                self.keyboard.press(KEY_NAME_TO_KEY[action[2]])
        if action[0] == 'release':
            if action[1] == 'char':
                self.keyboard.release(action[2])
            else:
                self.keyboard.release(KEY_NAME_TO_KEY[action[2]])

    def action_mouse(self, action_list, pause=None):
        self.reset(pause)
        self.stopper_var.start()
        while self.loop:
            if pause and self.count != 0:
                self.e_mouse(action_list[self.count], pause[self.count])
            elif pause and self.count == 0:
                self.e_mouse(action_list[self.count], self.median)
            else:
                self.e_mouse(action_list[self.count])
            self.count = (self.count + 1) % len(action_list)
        self.stopper_var.stop()

    def action_keyboard(self, action_list, pause=None):
        self.reset(pause)
        self.stopper_var.start()
        while self.loop:
            if action_list[self.count][2] == 'esc':
                pass
            else:
                if pause and self.count != 0:
                    self.e_keyboard(action_list[self.count], pause[self.count])
                elif pause and self.count == 0:
                    self.e_keyboard(action_list[self.count], self.median)
                else:
                    self.e_keyboard(action_list[self.count])
            self.count = (self.count + 1) % len(action_list)
        self.stopper_var.stop()
        for rel_char in VK_TO_CHAR.values():
            self.keyboard.release(rel_char)
            time.sleep(0.01)
        for rel_key in KEY_NAME_TO_KEY.values():
            self.keyboard.release(rel_key)
            time.sleep(0.01)

    def action_key_and_mousse(self, action_list, pause=None):
        self.reset(pause)
        self.stopper_var.start()
        while self.loop:
            if action_list[self.count][2] == 'esc':
                pass
            else:
                if action_list[self.count][0] == 'click' or action_list[self.count][0] == 'scroll':
                    if pause and self.count != 0:
                        self.e_mouse(action_list[self.count], pause[self.count])
                    elif pause and self.count == 0:
                        self.e_mouse(action_list[self.count], self.median)
                    else:
                        self.e_mouse(action_list[self.count])
                elif action_list[self.count][0] == 'press' or action_list[self.count][0] == 'release':
                    if pause and self.count != 0:
                        self.e_keyboard(action_list[self.count], pause[self.count])
                    elif pause and self.count == 0:
                        self.e_keyboard(action_list[self.count], self.median)
                    else:
                        self.e_keyboard(action_list[self.count])

            self.count = (self.count + 1) % len(action_list)
        self.stopper_var.stop()
        for rel_char in VK_TO_CHAR.values():
            self.keyboard.release(rel_char)
            time.sleep(0.01)
        for rel_key in KEY_NAME_TO_KEY.values():
            self.keyboard.release(rel_key)
            time.sleep(0.01)


click = [['click', (1040, 806), 'left'], ['click', (634, 736), 'left'], ['click', (719, 794), 'left'], ['click', (303, 364), 'left'], ['click', (303, 364), 'left'], ['click', (1102, 425), 'left'], ['click', (688, 499), 'left'], ['press', 'char', 'a'], ['press', 'char', 'u'], ['release', 'char', 'a'], ['release', 'char', 'u'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['click', (737, 556), 'left'], ['click', (592, 844), 'left'], ['click', (421, 966), 'left'], ['click', (404, 905), 'left'], ['click', (375, 953), 'left'], ['scroll', (1058, 897), [-3, 0]], ['click', (101, 879), 'left'], ['scroll', (103, 880), [-3, 0]], ['click', (1192, 810), 'left'], ['scroll', (1198, 810), [-3, 0]], ['click', (880, 561), 'left'], ['click', (1046, 817), 'left'], ['click', (726, 778), 'left'], ['click', (311, 786), 'left'], ['click', (311, 786), 'left'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 'm'], ['release', 'char', 'm'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'char', 't'], ['release', 'char', 't'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'j'], ['release', 'char', 'j'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'char', 'u'], ['release', 'char', 'u'], ['press', 'char', 'n'], ['press', 'char', 'b'], ['release', 'char', 'b'], ['release', 'char', 'n'], ['press', 'modifier', 'backspace'], ['release', 'modifier', 'backspace'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'modifier', 'enter'], ['release', 'modifier', 'enter'], ['press', 'char', 'p'], ['release', 'char', 'p'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'd'], ['release', 'char', 'd'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'p'], ['release', 'char', 'p'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'char', 'l'], ['release', 'char', 'l'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'm'], ['release', 'char', 'm'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 'c'], ['release', 'char', 'c'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'modifier', 'backspace'], ['release', 'modifier', 'backspace'], ['press', 'modifier', 'backspace'], ['release', 'modifier', 'backspace'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'modifier', 'enter'], ['release', 'modifier', 'enter'], ['press', 'char', 'f'], ['release', 'char', 'f'], ['press', 'char', 'é'], ['release', 'char', 'é'], ['press', 'char', 'd'], ['release', 'char', 'd'], ['press', 'char', 'é'], ['release', 'char', 'é'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'l'], ['release', 'char', 'l'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'g'], ['release', 'char', 'g'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'modifier', 'enter'], ['release', 'modifier', 'enter'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'char', 'g'], ['release', 'char', 'g'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 't'], ['release', 'char', 't'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'modifier', 'backspace'], ['release', 'modifier', 'backspace'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'modifier', 'backspace'], ['release', 'modifier', 'backspace'], ['press', 'modifier', 'backspace'], ['release', 'modifier', 'backspace'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'char', 't'], ['release', 'char', 't'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'modifier', 'space'], ['release', 'modifier', 'space'], ['press', 'char', 'l'], ['release', 'char', 'l'], ['press', 'char', 'o'], ['release', 'char', 'o'], ['press', 'char', 'g'], ['release', 'char', 'g'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 's'], ['release', 'char', 's'], ['press', 'char', 't'], ['release', 'char', 't'], ['press', 'char', 'i'], ['release', 'char', 'i'], ['press', 'char', 'q'], ['release', 'char', 'q'], ['press', 'char', 'u'], ['press', 'char', 'e'], ['release', 'char', 'u'], ['release', 'char', 'e'], ['press', 'modifier', 'enter'], ['release', 'modifier', 'enter'], ['click', (709, 942), 'left'], ['click', (707, 1006), 'left'], ['click', (1094, 525), 'left'], ['click', (1092, 516), 'left'], ['click', (238, 625), 'left'], ['click', (1091, 696), 'left'], ['click', (356, 748), 'left'], ['click', (356, 748), 'left'], ['click', (345, 922), 'left'], ['scroll', (1220, 791), [-3, 0]], ['click', (510, 575), 'left'], ['press', 'char', 'f'], ['release', 'char', 'f'], ['press', 'char', 'r'], ['release', 'char', 'r'], ['press', 'char', 'a'], ['release', 'char', 'a'], ['press', 'char', 'n'], ['release', 'char', 'n'], ['press', 'char', 'c'], ['release', 'char', 'c'], ['press', 'char', 'e'], ['release', 'char', 'e'], ['click', (363, 623), 'left'], ['click', (175, 780), 'left'], ['click', (172, 817), 'left'], ['scroll', (1198, 763), [-3, 0]], ['scroll', (74, 955), [-4, 0]], ['click', (165, 656), 'left'], ['click', (325, 893), 'left'], ['press', 'modifier', 'ctrl_l'], ['press', 'char', 'v'], ['release', 'char', 'v'], ['release', 'modifier', 'ctrl_l'], ['scroll', (1030, 850), [-1, 0]], ['scroll', (1179, 894), [-4, 0]], ['press', 'modifier', 'esc']]
time_pase = [1.2155413000000408, 3.905551600008039, 2.391004100005375, 3.556124800001271, 0.1648068000067724, 6.559012400000938, 1.4599904000060633, 1.2343073000083677, 0.07022939999296796, 0.030890800000634044, 0.034710100007941946, 0.14757879999524448, 0.07176809999509715, 0.0679186000052141, 0.09997029999794904, 2.001564699996379, 2.0611533999908715, 1.1768641999951797, 1.522208700000192, 0.7647695000050589, 1.541094799991697, 1.0139140999963274, 0.47598060000746045, 2.599106900001061, 0.5718811999977333, 2.233356199998525, 2.2506645000103163, 1.524994899999001, 1.3390023999963887, 0.9560746000061044, 5.054530900000827, 0.1028309000103036, 0.10023619999992661, 0.08382189999974798, 0.4159135000081733, 0.07612309999240097, 0.17192160000558943, 0.09205690000089817, 0.07187060000433121, 0.09628220000013243, 0.14791469999181572, 0.07589639999787323, 0.035925000003771856, 0.0679904999997234, 0.09235380000609439, 0.07207629999902565, 0.13574579999840353, 0.08377110000583343, 0.07193120000010822, 0.08801050001056865, 0.1283046999888029, 0.11177930000121705, 0.12095599999884143, 0.09204869999666698, 0.08799379999982193, 0.0759472000063397, 0.320044299995061, 0.004455999995116144, 0.018468700000084937, 0.01706680000643246, 1.0119373000052292, 0.08403880000696518, 0.2844161999964854, 0.07982230000197887, 0.19179409999924246, 0.0680932999966899, 0.07983270000841003, 0.06845720000274014, 0.09964810000383295, 0.08056640000722837, 0.4798110999981873, 0.07175200000347104, 1.973474400001578, 0.09579920000396669, 0.2754694000032032, 0.10809470000094734, 0.17601229999854695, 0.08128910000959877, 0.0996673999907216, 0.07629549999546725, 0.12793869999586605, 0.05975590000161901, 0.1319404000096256, 0.10010619999957271, 0.028587000007973984, 0.06349890001001768, 0.09241549999569543, 0.0754218999936711, 0.019927999994251877, 0.07997310000064317, 0.08417570000165142, 0.07191169999714475, 0.004200199997285381, 0.1039011999964714, 0.1039664999989327, 0.06821900000795722, 0.039973299994017, 0.059716100004152395, 0.11601769999833778, 0.07995059998938814, 0.004028699986520223, 0.08797969999432098, 0.027997400000458583, 0.09215039999980945, 0.09187120001297444, 0.08406179999292362, 0.1559421999991173, 0.07597779999196064, 0.20403219999570865, 0.05193580000195652, 0.0840254999930039, 0.04805889999261126, 0.08799220000219066, 0.0609594000125071, 0.3438469999964582, 0.0891029000049457, 0.0749923000112176, 0.08797279999998864, 0.008351500000571832, 0.0997471000009682, 0.051962999990792014, 0.08802140000625513, 0.5802822999976343, 0.07959240001218859, 1.7328453999944031, 0.11131809999642428, 0.41192640000372194, 0.09201259999827016, 0.1922346000064863, 0.09571769999456592, 0.12803710000298452, 0.11680520001391415, 0.08711250001215376, 0.07227819999388885, 0.12406129999726545, 0.0718124999984866, 0.12801289999333676, 0.07200850000663195, 0.2398413999908371, 0.09196019999217242, 0.07625310000730678, 0.07195679999131244, 0.028102800002670847, 0.06822660000761971, 0.11968260000867303, 0.0599142999999458, 0.020170900010270998, 0.09970089999842457, 0.0602253999968525, 0.06786480000300799, 0.1250101000041468, 0.0842253000009805, 0.06394839999848045, 0.07181870000204071, 0.06011859999853186, 0.08389200000965502, 0.7759744999930263, 0.11196290000225417, 0.6526513999997405, 0.08340569998836145, 0.08791129999735858, 0.07218230000580661, 0.13985910000337753, 0.06806010000582319, 0.16800689999945462, 0.11990350000269245, 0.06400170001143124, 0.08400129999790806, 0.09249540000746492, 0.08753789999173023, 0.09222299999964889, 0.08769999998912681, 0.06065370001306292, 0.08770360000198707, 0.48759839999547694, 0.09199570000055246, 0.07646509999176487, 0.09176500000467058, 0.7799053000053391, 0.09992189999320544, 0.07199390001187567, 0.1001955999963684, 0.36543999999412335, 0.10341670000343584, 0.06796559999929741, 0.12397989998862613, 0.16401379999297205, 0.07202289999986533, 0.016264500009128824, 0.06765889999223873, 0.0840433999983361, 0.07604139999602921, 0.14000189999933355, 0.06800119999388698, 0.03990230000636075, 0.08828440000070259, 0.09179950000543613, 0.07191539999621455, 0.1121277999918675, 0.07593000000633765, 0.09601960000873078, 0.0720996999880299, 0.08401789999334142, 0.07187610000255518, 0.1759639999945648, 0.0560226999950828, 0.10411620000377297, 0.05602439999347553, 0.1918773999932455, 0.07205479999538511, 0.07600199998705648, 0.10392669998691417, 0.0479637999960687, 0.048066400006064214, 0.016059899993706495, 0.08783359998778906, 0.6250657999917166, 0.06392709999636281, 1.5017623999883654, 2.1559660000057193, 2.260045999995782, 0.9218459999974584, 1.9919912999903318, 2.0840235999930883, 1.5830451999936486, 0.5820093999936944, 1.8039542000042275, 1.2579526999907102, 1.5160821000026772, 1.0049788000033004, 0.06335189999663271, 0.11603980000654701, 0.06799120000505354, 0.12405399999988731, 0.09638930000073742, 0.07173510000575334, 0.05675570000312291, 0.06000849998963531, 0.08007020001241472, 0.09603919999790378, 0.07991590000165161, 2.6907724000047892, 3.2049389999883715, 1.1338809999870136, 0.8349542999931145, 1.7320023000065703, 1.4790259000001242, 1.6790187000005972, 1.336333500003093, 0.06058749998919666, 0.07232099999964703, 0.1395992999896407, 5.4510807000042405, 0.20020140000269748, 2.0408499000041047, 4.]

exe_module = Executor()
exe_module.action_key_and_mousse(click, time_pase)