# -*- coding: utf-8 -*-

__author__ = "Nicholas Murray"

import klibs
from klibs import P
from klibs.KLGraphics import KLDraw as kld # To draw shapes
from klibs.KLUserInterface import any_key # So participants can press any key to continue
from klibs.KLGraphics import fill, blit, flip # To actually make drawn shapes appear on the screen
from klibs.KLUtilities import deg_to_px # Convert stimulus sizes according to degrees of visual angle
from klibs.KLResponseCollectors import KeyPressResponse # To take in key presses as a response to a trial
from klibs.KLResponseListeners import KeypressListener # To record key press responses at the end of a trial
from klibs.KLConstants import TK_MS # to specify milliseconds as the unit of time to measure response times in

# Defining some useful constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (45, 45, 45)

class gaze_ilm(klibs.Experiment):

    def setup(self):
        # Fixation Cross
        crosslinesize = deg_to_px(.57)
        self.horizontal_cross = kld.Line(length = crosslinesize, color = WHITE, thickness = 3)
        self.vertical_cross = kld.Line(length = crosslinesize, color = WHITE, thickness = 3, rotation = 90)

        # X which replaces the fixation cross on exogenous cuing trials
        self.x_cross1 = kld.Line(length = crosslinesize, color = WHITE, thickness = 3, rotation = 45)
        self.x_cross2 = kld.Line(length = crosslinesize, color = WHITE, thickness = 3, rotation = -45)

        # Probe stimuli
        probecirclesize = deg_to_px(.57)
        innercirclesize = deg_to_px(.4)
        probestroke = [1, (0,0,0)]
        probe_horizontal_offset = deg_to_px(5)
        probe_vertical_offset = deg_to_px(1.1)
        self.probecircle = kld.Circle(diameter = probecirclesize, stroke = probestroke, fill = WHITE)
        self.innercircle = kld.Circle(diameter = innercirclesize, stroke = probestroke, fill = GREY)
        self.left_probe_position = (P.screen_c[0]-probe_horizontal_offset, P.screen_c[1]-probe_vertical_offset)
        self.right_probe_position = (P.screen_c[0]+probe_horizontal_offset, P.screen_c[1]-probe_vertical_offset)
        
        # Exogenous cue stimuli
        cue_stroke_thickness = 2
        self.cue = kld.Circle(diameter = probecirclesize, stroke = [cue_stroke_thickness, WHITE], fill = WHITE)

        # Detection target stimuli
        targetsize = deg_to_px(.23)
        targetstroke = [1, (0,0,0)]
        self.target = kld.Circle(diameter = targetsize, stroke = targetstroke, fill = WHITE)

    #######################################################################################
        # FUNCTIONS DEFINING THE EXOGENOUS CUING TASK STIMULI
    #######################################################################################

    def trial_start_stimuli(self):
        # Fixation cross
        fill()
        blit(self.horizontal_cross, registration = 5, location = P.screen_c)
        blit(self.vertical_cross, registration = 5, location = P.screen_c)

        # Probes
        blit(self.probecircle, registration = 5, location = self.left_probe_position)
        blit(self.probecircle, registration = 5, location = self.right_probe_position)
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)
        flip()

    def exo_trial_pre_cue_stimuli(self):
        # X-cross
        fill()
        blit(self.x_cross1, registration = 5, location = P.screen_c)
        blit(self.x_cross2, registration = 5, location = P.screen_c)

        # Probes
        blit(self.probecircle, registration = 5, location = self.left_probe_position)
        blit(self.probecircle, registration = 5, location = self.right_probe_position)
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)
        flip()

    def exo_trial_left_cue_stimuli(self):
        # X-cross
        fill()
        blit(self.x_cross1, registration = 5, location = P.screen_c)
        blit(self.x_cross2, registration = 5, location = P.screen_c)

        # Probes
        blit(self.probecircle, registration = 5, location = self.right_probe_position)
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)

        # Left exogenous cues
        blit(self.cue, registration = 5, location = self.left_probe_position)

        flip()

    def exo_trial_right_cue_stimuli(self):
        # X-cross
        fill()
        blit(self.x_cross1, registration = 5, location = P.screen_c)
        blit(self.x_cross2, registration = 5, location = P.screen_c)

        # Probes
        blit(self.probecircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)

        # Right exogenous cues
        blit(self.cue, registration = 5, location = self.right_probe_position)

        flip()

    def exo_trial_neutral_cue_stimuli(self):
        # X-cross
        fill()
        blit(self.x_cross1, registration = 5, location = P.screen_c)
        blit(self.x_cross2, registration = 5, location = P.screen_c)

        # Probes
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)

        # Left and right exogenous cue simultaneously (i.e., neutral exogenous cue)
        blit(self.cue, registration = 5, location = self.left_probe_position)
        blit(self.cue, registration = 5, location = self.right_probe_position)

        flip()

    def exo_trial_left_target_stimuli(self):
        # X-cross
        fill()
        blit(self.x_cross1, registration = 5, location = P.screen_c)
        blit(self.x_cross2, registration = 5, location = P.screen_c)

        # Probes
        blit(self.probecircle, registration = 5, location = self.left_probe_position)
        blit(self.probecircle, registration = 5, location = self.right_probe_position)
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)

        # Left detection target
        blit(self.target, registration = 5, location = self.left_probe_position)
        flip()

        response = self.rc.keypress_listener.response(rt = False) # get the response value
        rt = self.rc.keypress_listener.response(value = False) # get the reaction time

    def exo_trial_right_target_stimuli(self):
        # X-cross
        fill()
        blit(self.x_cross1, registration = 5, location = P.screen_c)
        blit(self.x_cross2, registration = 5, location = P.screen_c)

        # Probes
        blit(self.probecircle, registration = 5, location = self.left_probe_position)
        blit(self.probecircle, registration = 5, location = self.right_probe_position)
        blit(self.innercircle, registration = 5, location = self.left_probe_position)
        blit(self.innercircle, registration = 5, location = self.right_probe_position)

        # Right detection target
        blit(self.target, registration = 5, location = self.right_probe_position)
        flip()

        response = self.rc.keypress_listener.response(rt = False) # get the response value
        rt = self.rc.keypress_listener.response(value = False) # get the reaction time

    #######################################################################################

    def block(self):
        pass

    def setup_response_collector(self):
        self.rc.uses(KeyPressResponse) # Specify to record key presses
        self.rc.terminate_after = [1700, TK_MS] # End the collection loop after 1700 ms
        #self.rc.display_callback = self.resp_callback # Run the self.resp.callback method every loop
        self.rc.flip = True # draw the screen at the end of every loop
        self.rc.keypress_listener.key_map = {'z': "left", '/': "right"} # Interpret Z-key presses as "left", /-key presses as "right"
        self.rc.keypress_listener.interrupts = True # end the collection loop if a valid key is pressed

    def trial_prep(self):
        pass

    def trial(self):

        self.exo_trial_right_target_stimuli()

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass
