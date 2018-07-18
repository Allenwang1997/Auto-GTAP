__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-5-4"

from AutoGTAP.Shocks.Shocks import Shocks


class GTAPAdjustCMF(object):
    """Creates an CMF file for controlling gemsim when it runs the GTAP adjust (as opposed to the policy simulation)"""

    __slots__ = ["simulation_name", "solution_method", "model_folder", "shock_type"]

    def __init__(self, simulation_name: str, solution_method: str, model_folder: str, shock_type: str) -> None:
        self.solution_method = solution_method
        self.model_folder = model_folder
        self.shock_type = shock_type
        self.simulation_name = simulation_name

        cmf_file_name = "gtapadjust.cmf"

        line_list_main = [
            'auxiliary files = GtapAdjust;',
            '!check-on-read elements = warn; ! Optional: very often needed',
            'cpu=yes ; ! Optional: Reports CPU times for various stages',
            'log file = GtapAdjust.log;  ! Optional',
            '! input files:',
            'File INFILE = work\orig.har; ! Normalized GTAP data - containing flows and sets',
            '! Output files:',
            'File Initial = work\InitialRpt.har; ! Diagnostic output for pre-adjustment data',
            'File Final   = work\FinalRpt.har;   ! Diagnostic output for post-adjustment data',
            'Solution File = work\\adjust;        ! Diagnostic output ',
            '! Updated files:',
            'Updated File INFILE = work\\adjusted.har; ! Adjusted Normalized GTAP data ',
            '',
            '! Solution method',
            'method = Euler ;',
            'steps = 6;',
            'start with mmnz = 2000000;',
            '',
            '! Automatic closure generated by TABmate Tools...Closure command',
            '!              Variable     Size ',
            'Exogenous      domslack ; ! IND*REG   slack to scale all flows entering into COSTS so that COSTS=SALES',
            'Exogenous      impslack ; ! COM*REG   Slack to scale TRADE to balance Regional imports',
            'Exogenous      marslack ; ! MAR   Slack to scale VST to balance supply/demand of shipping margins',
            'Exogenous      q1absorp ; ! FIN*REG   GDP/absorption link variable',
            'Exogenous      q3absorp ; ! 1   World GDP/absorption link variable',
            'Exogenous          qdem ; ! COM*REG   scales ALL use of c made in f',
            'Exogenous          qexp ; ! COM*REG   Export factor: use to target exports',
            'Exogenous       qexpend ; ! FIN*REG   Absorption factors: to target C, I, G',
            '!Exogenous        qtrdbi ; ! COM*REG*REG   scales exports from f to t [to target vTRADE_FOB]',
            'Exogenous       qexptot ; ! REG   Export factor: use to target aggregate exports',
            'Exogenous          qfac ; ! FAC*REG   to target [parts of] vGDPFACS(f,r)',
            'Exogenous          qimp ; ! COM*REG   Import factor: use to target imports',
            'Exogenous       qimptot ; ! REG   Import factor: use to target aggregate imports',
            'Exogenous       qnatsiz ; ! REG   Size factor: use to target national GDP',
            'Exogenous       qNATTAX ; ! COM*REG   to target NATTAX',
            'Exogenous    qNATTAXTOT ; ! REG   to target NATTAXTOT',
            'Exogenous       qTRDTAX ; ! COM*TRD*REG   to target TRDTAX',
            'Exogenous    qTRDTAXTOT ; ! TRD*REG   to target TRDTAXTOT',
            'Rest endogenous; ! end of TABmate automatic closure',
            '',
            '!    old exog      new exog   !   ',
            'swap  domslack = dDOMCHECK;  ! scale industry costs to force costs=sales',
            'swap  impslack = dIMPCHECK;  ! scale trade matrix to force supply=demand for imports',
            'swap  marslack = dMARCHECK;  ! scale VST matrix to force supply=demand for shipping',
            '',
            '! remove pre-existing imbalances !',
            'final_level  dDOMCHECK = uniform 0;   ! force costs=sales',
            'final_level  dIMPCHECK = uniform 0;   ! force supply=demand for imports',
            'final_level  dMARCHECK = uniform 0;   ! force supply=demand for shipping',
            '',
            '! Optional link to make absorption follow GDP: use with caution (see TAB)',
            '!    old exog      new exog   !   ',
            '!swap  q1absorp = q2absorp;  ! optional: link aborption to GDP ',
            '!swap  q3absorp = vGDPWLD;   ! needed if q2absorb exogenous; fix world GDP  ',
            '',
            '!********** YOU SHOULD NORMALLY EDIT ONLY BELOW THIS LINE ***********! '
        ]

        # line_list_shocks_original = [
        #     '',
        #     '!    old exog                new exog   !   ',
        #     'swap qdem("omn","Australia")=vCOSTS("omn","Australia");',
        #     'final_level  vCOSTS("omn","Australia")= 50000; ',
        #     '',
        #     '!    old exog      new exog   !   ',
        #     '!swap qEXP("foodfrsfsh","Australia")=vEXPDEM("foodfrsfsh","Australia");',
        #     '!final_level  vEXPDEM("foodfrsfsh","Australia") = 40000;  ',
        #     '',
        #     '!    old exog      new exog   !   ',
        #     '!swap qimp("foodfrsfsh","Australia")=vIMPCIF("foodfrsfsh","Australia");',
        #     '!final_level  vIMPCIF("foodfrsfsh","Australia") = 10000;  ',
        #     '',
        #     '!    old exog      new exog   !   ',
        #     '!swap qexptot("Australia")=vGDPEXPS("Exp","Australia");',
        #     '!final_level  vGDPEXPS("Exp","Australia") = 170000;  ',
        #     '',
        #     '!    old exog      new exog   !   ',
        #     '!swap qtrdtax("omn","exp","Australia")=vTRDTAX("omn","exp","Australia");',
        #     '!final_level  vTRDTAX("omn","exp","Australia")= 12; ',
        #     ' ',
        #     '!    old exog      new exog   !   ',
        #     '!swap qtrdtax("foodfrsfsh","imp","Australia")=vTRDTAX("foodfrsfsh","imp","Australia");',
        #     '!final_level  vTRDTAX("foodfrsfsh","imp","Australia")= 200;  ',
        #     '',
        #     '!    old exog      new exog   !   ',
        #     '!swap qnattaxtot("Australia")=vNATTAXTOT("Australia");',
        #     '!final_level  vNATTAXTOT("Australia")= 50000;  ',
        #     '',
        #     'Verbal Description = Adjust GTAP database  ;'
        # ]

        line_list_shocks = Shocks(self.shock_type).create()

        # Combine line lists
        line_list_total = line_list_main + line_list_shocks

        # Create final file
        cmf_file_name_with_path = "WorkFiles\\" + self.simulation_name + "\\" + self.model_folder + "\\input\\" + cmf_file_name
        with open(cmf_file_name_with_path, "w+") as writer:  # Create the empty file
            writer.writelines(line +'\n' for line in line_list_total)  # write the line list to the file
