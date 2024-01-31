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
from klibs.KLEventInterface import TrialEventTicket as ET # to define the events of a trial according to stimulus timings
from klibs.KLKeyMap import KeyMap # To map keys to responses and have them recorded in the database
import sdl2 # To generate keyboard button names upon pressing them as a response
from klibs.KLCommunication import message # To write messages on the screen to participants

# Defining some useful constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (45, 45, 45)

class gaze_ilm(klibs.Experiment):

    def setup(self):
        # Block and trial start messages
        self.block_start_message = message("Press space to begin the experiment", "default", blit_txt = False)
        self.next_trial_message = message("Press space to continue", "default", blit_txt = False)

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

    def exo_cuing_task(self):
        while self.evm.before("x_cross_on"):
            self.trial_start_stimuli()
        
        while(self.evm.between("x_cross_on", "cue_onset")):
            self.exo_trial_pre_cue_stimuli()

        while self.evm.between("cue_onset", "cue_offset"):
            if self.cue_location == "left":
                self.exo_trial_left_cue_stimuli()
            else:
                if self.cue_location == "right":
                    self.exo_trial_right_cue_stimuli()
                else:
                    self.exo_trial_neutral_cue_stimuli()
        
        while self.evm.between("cue_offset", "target_onset"):
            self.exo_trial_pre_cue_stimuli()

        while self.evm.between("target_onset", "target_offset"):
            if self.target_location == "left": 
                self.exo_trial_left_target_stimuli()
            else:
                self.exo_trial_right_target_stimuli()

        while self.evm.between("target_offset", "trial_end"): 
            self.exo_trial_pre_cue_stimuli()

    #######################################################################################

    def block(self):
        pass

    def setup_response_collector(self):
        self.rc.uses(KeyPressResponse) # Specify to record key presses
        self.rc.terminate_after = [5000, TK_MS] # End the collection loop after 1700 ms
        #self.rc.display_callback = self.resp_callback # Run the self.resp.callback method every loop
        self.rc.flip = True # draw the screen at the end of every loop
        self.rc.keypress_listener.key_map = KeyMap('response', ['z', '/'], ['left', 'right'], [sdl2.SDLK_z, sdl2.SDLK_SLASH]) # Interpret Z-key presses as "left", /-key presses as "right"
        self.rc.keypress_listener.interrupts = True # end the collection loop if a valid key is pressed

    def trial_prep(self):

        # Define stimulus event timings
        events = []
        events.append([100, "x_cross_on"]) # Add in the x-cross after fixation
        events.append([events[-1][0] + 400, "cue_onset"]) # Add in the cue
        events.append([events[-1][0] + 50, "cue_offset"]) # Remove the cue
        events.append([events[-1][0] + 50, "target_onset"]) # Add in the target
        events.append([events[-1][0] + 50, "target_offset"]) # Remove the target
        events.append([events[-1][0] + 1700, "trial_end"])

        for e in events:
            self.evm.register_ticket(ET(e[1], e[0]))

        # If the first trial of the block, display message to start.
        if P.trial_number == 1:
            fill()
            blit(self.block_start_message, registration = 5, location = P.screen_c)
            flip()
            any_key()

        #if P.trial_number > 1:
            #fill()
            #blit(self.next_trial_message, registration = 5, location = P.screen_c)
            #flip()
            #any_key()

    def trial(self):

        self.exo_cuing_task()

        self.rc.collect()
        rt = self.rc.keypress_listener.response(False, True)
        response = self.rc.keypress_listener.response(True, False)
    
        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "reaction_time": rt,
            "response": response,
            "cue_location": self.cue_location,
            "target_location": self.target_location
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass
