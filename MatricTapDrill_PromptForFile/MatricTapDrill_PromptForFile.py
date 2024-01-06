#Author- BCD Sim
#Description-  Imports a JSON file from a user prompt and creates metric tap drill sizes user parameters for each size.

import adsk.core, adsk.fusion, adsk.cam, traceback
import json

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # Create a file dialog to prompt the user for a file
        fileDialog = ui.createFileDialog()
        fileDialog.title = "Select JSON File"
        fileDialog.filter = 'JSON files (*.json)|*.json;'
        dialogResult = fileDialog.showOpen()

        # If the user cancels the file dialog, stop the script
        if dialogResult == adsk.core.DialogResults.DialogOK:
            file = fileDialog.filename
        else:
            return
        
        # Initialize empty lists
        sizes = []
        drills = []
        radial_engagements = []
        drill_alternates = []
        radial_engagement_alternates = []

        with open(file, 'r') as json_file:
            data = json.load(json_file)

        for key in data:
            sizes.append(data[key]['Size'])
            drills.append(data[key]['drill'])
            radial_engagements.append(data[key]['radialEngagement'])
            drill_alternates.append(data[key]['drillAlternate'])
            radial_engagement_alternates.append(data[key]['radialEngagementAlternate'])

        for index in range(len(sizes)):
            pName = (sizes[index].replace('.', '_') + '_tap_drill')  
            pUnit = 'mm'
            pExpression = float(drills[index])
            pComment = ('Tap Drill Size for ' + str(sizes[index]) + 
                        ' with ' + str(radial_engagements[index]) + ' radial engagement.' + 
                        'Alternate drill size is ' + str(drill_alternates[index]) + 
                        ' with ' + str(radial_engagement_alternates[index]) + ' radial engagement.')

            # Convert the float to a string, split it, apply zfill to the parts, and join them back together
            pExpressionStr = str(pExpression)
            parts = pExpressionStr.split('.')
            pExpressionFormatted = '.'.join(part.zfill(2) if part.isdigit() else part for part in parts)
            pExressionReal = adsk.core.ValueInput.createByString(pExpressionFormatted)
           
            design.userParameters.add(pName, pExressionReal, pUnit, pComment)

        ui.messageBox('Metric Tap Drill Parameters Created')
 
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
