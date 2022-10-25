VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} ResourceQuery 
   Caption         =   "Resource Query"
   ClientHeight    =   7035
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   11505
   OleObjectBlob   =   "ResourceQuery.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "ResourceQuery"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub UserForm_Initialize()
'VARIABLES
Dim table_name As String
Dim table_range As Range
Dim lo As ListObject
Dim filtered_range As Range
Dim skillsets_length As Integer
Dim skillsets As New ArrayList
Dim skillsets_temp() As String 'create a temp array to hold split skillsets

'SETUP
ResourceQuery.Caption = "Resource Query"
table_name = "directory_table"
'Set table_range = Directory.Range("directory_table")
Set lo = Directory.ListObjects(table_name)
'table_range = Range(table_name)

'WORK
lo.AutoFilter.ShowAllData 'clear filters from table
'Set filtered_range = Directory.Range(table_name).SpecialCells(xlCellTypeVisible)

'add each skillset to arrayList skillsets()
'On Error GoTo hell
'For Each cell In filtered_range 'for each cell in table
'    If (cell.Column = 3) Then 'if activecell column is 3
'        'if cell contains multipe skillsets
'        On Error GoTo hath
'        If (InStr(cell.Value, " ") > 0) Then 'if cell contains a space
'            'skillsets_temp() = Split(cell.Value, " ") 'add skillsets in cell to temp array
'            On Error GoTo no
'            For Each skillset In skillsets_temp 'for each skillet in cell
'                If Not (skillsets.Contains(skillset)) Then 'If skillsets() does not contain skillset
'                    'skillsets.Add (skillset) 'add skillset to array
'                End If
'            Next
'        Else 'only one skillset - no spaces
'            On Error GoTo fury
'            If Not (skillsets.Contains(cell.Value)) Then 'If skillsets() does not contain skillset
'                'skillsets.Add (cell.Value) 'add skillset to array
'            End If
'        End If
'    End If
'Next
   
'add the skillsets to the skillset_combo_box
For Each skillset In Sheet8.Range("key")
    skillset_combo_box.AddItem (skillset.Value)
Next

'add the from_locations to the from_combo_box
For Each result In Sheet8.Range("from")
    from_combo_box.AddItem (result.Value)
Next

type_combo_box.AddItem ("Resource")
type_combo_box.AddItem ("Tool")
type_combo_box.AddItem ("Training Resource")
type_combo_box.AddItem ("")


End Sub

Private Sub query_go_Click()
'variables
Dim query As String
Dim table_name As String
Dim table_range As Range
Dim results_count As Integer
Dim filtered_range As Range

'setup
query = query_entry.Value
table_name = "directory_table"
Set table_range = Directory.Range("directory_table")
'Directory.ListObjects.Add(xlSrcRange, table_range, xlListObjectHasHeaders:=xlYes).Name = table_name 'creates a table from range
Dim lo As ListObject
Set lo = Directory.ListObjects(table_name)

'methods
results_list_box.Clear 'clear list box
lo.AutoFilter.ShowAllData 'clear filters from table
lo.Sort.Apply 'sort table

If (skillset_combo_box.Value = "" Or skillset_combo_box.Value = "All") Then 'if no skillset selected
    lo.Range.AutoFilter Field:=1, Criteria1:=("*" + query + "*") 'filter by query
ElseIf (Not skillset_combo_box.Value = "") Then 'if skillset selected
    lo.Range.AutoFilter Field:=1, Criteria1:=("*" + query + "*") 'filter by query
    lo.Range.AutoFilter Field:=5, Criteria1:=("*" + skillset_combo_box.Value + "*") 'filter skillset
End If

If (Not type_combo_box.Value = "") Then 'if type selected
    lo.Range.AutoFilter Field:=4, Criteria1:=("*" + type_combo_box.Value + "*") 'filter skillset
End If

If (Not from_combo_box.Value = "") Then   'if from selected
    lo.Range.AutoFilter Field:=3, Criteria1:=("*" + from_combo_box.Value + "*") 'filter from
Else
    
End If

On Error GoTo hell
Set filtered_range = Directory.Range(table_name).SpecialCells(xlCellTypeVisible) 'assign the range for results

'Display filtered results {
With results_list_box
    .ColumnCount = 2 'set 2 columns
    .ColumnWidths = "350;60" 'set column width
    For Each cell In filtered_range 'for each visible result
        If (cell.Column = "2") Then
            .AddItem (cell.Value)
        ElseIf (cell.Column = "4") Then
            .List(.ListCount - 1, 1) = cell.Value
        End If
    Next cell
End With
' End display
    
Done:
    Exit Sub
    
hell:
    MsgBox ("No Links Found, please try a simpler query.")
    lo.AutoFilter.ShowAllData 'clear filters from table

End Sub
Private Sub results_list_box_DblClick(ByVal Cancel As MSForms.ReturnBoolean)
'variables
Dim query_string As String
Dim smart_address As String

'setup
query_string = results_list_box.Text
smart_address = Application.WorksheetFunction.VLookup(query_string, Directory.Range("directory_table"), 2, False)

'method
OpenURLInFF (smart_address)
End Sub

Sub OpenURLInFF(ByVal sURL As String)
    On Error GoTo Error_Handler
    Dim WSHShell              As Object
    Dim sFFExe                As String    'FF executable path/filename
 
    'Determine the Path to FF executable
    Set WSHShell = CreateObject("WScript.Shell")
    sFFExe = WSHShell.RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Firefox.EXE\")
    'Open the URL
    Shell """" & sFFExe & """" & " -new-tab """ & sURL & "", vbHide
 
Error_Handler_Exit:
    On Error Resume Next
    If Not WSHShell Is Nothing Then Set WSHShell = Nothing
    Exit Sub
 
Error_Handler:
    If Err.Number = -2147024894 Then
        MsgBox "FireFox does not appear to be installed on this compter", _
               vbInformation Or vbOKOnly, "Unable to open the requested URL"
    Else
        MsgBox "The following error has occurred" & vbCrLf & vbCrLf & _
               "Error Number: " & Err.Number & vbCrLf & _
               "Error Source: OpenURLInFF" & vbCrLf & _
               "Error Description: " & Err.Description & _
               Switch(Erl = 0, "", Erl <> 0, vbCrLf & "Line No: " & Erl) _
               , vbOKOnly + vbCritical, "An Error has Occurred!"
    End If
    Resume Error_Handler_Exit
End Sub
