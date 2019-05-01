# DirectoryTools for Flame v1.0
# Copyright (c) 2019 Bob Maple (bobm-matchbox [at] idolum.com)
#
# For Flame 2020 and above - place in /opt/Autodesk/shared/python/
#
# Adds a submenu to the MediaHub context menu in Files mode to tar and zip
# a selected directory or directories (makes separate files for each)
#
# Select a directory in the browser and right-click to access

# git push -u origin master


##### First some helper-monkeys
#####

def ask_yesno( dlg_msg, dlg_title ) :
  from PySide2.QtWidgets import QMessageBox

  qtMsgBox = QMessageBox()
  qtMsgBox.setWindowTitle( dlg_title )
  qtMsgBox.setText( dlg_msg )
  qtMsgBox.setStandardButtons( QMessageBox.Yes | QMessageBox.Cancel )
  qtMsgBox.setDefaultButton( QMessageBox.Yes )
  res = qtMsgBox.exec_()

  if res == QMessageBox.Cancel :
  	return( False )
  else:
  	return( True )

#

def ask_password() :
  from PySide2 import QtWidgets, QtGui

  encPW, okBut = QtWidgets.QInputDialog.getText( None, "Password", "Encryption Password (leave blank or Cancel for none):" )

  if okBut and encPW:
    return( True, encPW )
  else:
    return( False, False )


##### Main Flame hook handler
#####

def get_mediahub_files_custom_ui_actions():
  import os, subprocess, time, tempfile

  def menu_enabled(sel) :
    if os.path.isdir( sel[0] ) :
      return True
    else :
      return False

  #

  def tardir_go(sel) :

    for curitem in sel :
      if os.path.isdir( curitem.path ) :
        archive_dest, archive_dir, archive_file, archive_pathname = makepaths( curitem, ".tar" )

        do_it = True

        if ask_yesno( "Create " + archive_pathname + " ?", "tar directory" ) :
          if os.path.isfile( arhive_pathname ) :
            if not ask_yesno( "Overwrite " + archive_pathname + " ?", archive_file + " exists" ) :
            	do_it = False
        else:
          do_it = False

        if do_it :
          tmpFP, tmpName = tempfile.mkstemp( ".sh", "flametar" )
          os.write( tmpFP, '#!/bin/sh\n' )
          os.write( tmpFP, 'cd "' + archive_dest + '"\n' )
          os.write( tmpFP, 'tar -cf "' + archive_file + '" "' + archive_dir + '"\n' )
          os.write( tmpFP, 'tar -tf "' + archive_file + '" > "' + archive_file + '.list"\n' )
          os.write( tmpFP, 'rm "' + tmpName + '"\n' )
          os.close( tmpFP )

          tar_cmd = [ "/bin/sh", tmpName ]
          rc = subprocess.Popen( tar_cmd )

  #

  def zipdir_go(sel) :

    for curitem in sel :
      if os.path.isdir( curitem.path ) :
        archive_dest, archive_dir, archive_file, archive_pathname = makepaths( curitem, ".zip" )

        do_it = True

        if ask_yesno( "Create " + archive_pathname + " ?", "zip directory" ) :
          if os.path.isfile( arhive_pathname ) :
            if not ask_yesno( "Overwrite " + archive_pathname + " ?", archive_file + " exists" ) :
              do_it = False
        else:
          do_it = False

        if do_it :
          doPW, usePW = ask_password()

          tmpFP, tmpName = tempfile.mkstemp( ".sh", "flamezip" )
          os.write( tmpFP, '#!/bin/sh\n' )
          os.write( tmpFP, 'cd "' + archive_dest + '"\n' )
          os.write( tmpFP, 'zip -r -q ' + ('-e P "' + usePW + '" ') if doPW else '' )
          os.write( tmpFP, '"' + archive_file + '_busy" "' + archive_dir + '"\n' )
          os.write( tmpFP, 'mv "' + archive_file + '_busy" "' + archive_file + '"\n' )
          os.write( tmpFP, 'rm "' + tmpName + '"\n' )
          os.close( tmpFP )

          zip_cmd = [ "/bin/sh", tmpName ]
          # rc = subprocess.Popen( zip_cmd )

  #

  def make_paths( item, extension ) :
    # Takes a Flame object and returns a tuple:
    # destination path, directory to archive, filename of archive, full pathname of archive

    cur_dir, junk = os.path.split( item.path )
    archive_dest, archive_dir = os.path.split( cur_dir )
    archive_file = archive_dir + extension
    archive_path = os.path.join( archive_dest, archive_file )

    print( "archive_dest: " + archive_dest )
    print( "archive_dir : " + archive_dest )
    print( "archive_file: " + archive_dest )
    print( "archive_path: " + archive_dest )

    return( archive_dest, archive_dir, archive_file, archive_path )


#

return [
  {
    "name": "Directory Tools",
    "actions": [
      {
        "name": "TAR Directory",
        "isEnabled": menu_enabled,
        "execute": tardir_go
      },
      {
        "name": "ZIP Directory",
        "isEnabled": menu_enabled,
        "execute": zipdir_go
      }
    ]
  }
]
