VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} VATool 
   Caption         =   "VA Tool"
   ClientHeight    =   1470
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   6855
   OleObjectBlob   =   "VATool.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "VATool"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub go_button_Click()
'''variables
Dim lo As ListObject
Dim filtered_range As Range

'''setup
Set lo = VA_Full.ListObjects("Table2")
lo.AutoFilter.ShowAllData 'clear filters from table
lo.Sort.Apply 'sort table

'''action
If (active_status_cb.Value = "" And passive_status_cb.Value = "" And indicator_cb.Value = "") Then
    MsgBox ("Please select a value for each field and try again")
Else
    lo.Range.AutoFilter Field:=1, Criteria1:=("*" + active_status_cb.Value + "*") '
    lo.Range.AutoFilter Field:=2, Criteria1:=("*" + passive_status_cb.Value + "*") '
    lo.Range.AutoFilter Field:=3, Criteria1:=("*" + indicator_cb.Value + "*") '
    
    On Error GoTo hell
    Set filtered_range = VA_Full.Range("Table2").SpecialCells(xlCellTypeVisible) 'assign the range for results
    
    For Each cell In filtered_range
        If cell.Column = "5" Then
            MsgBox cell.Value, , "Poro"
        End If
    Next
End If

Done:
    Exit Sub
    
hell:
    MsgBox ("No Results Found")
    lo.AutoFilter.ShowAllData 'clear filters from table
End Sub

Private Sub UserForm_Initialize()
'''Variables
Dim active_count As Integer
Dim list_length As Integer
Dim active_status_array As New ArrayList
Dim passive_status_array As New ArrayList
Dim indicator_array As New ArrayList
Dim lo As ListObject

'''Setup
active_count = 0
VATool.Caption = "VA Tool"
list_length = VA_Full.Range("active_status_list").Count
Set lo = VA_Full.ListObjects("Table2")
lo.AutoFilter.ShowAllData

'''Action
active_status_cb.Clear

'Store options in arrays
For i = 0 To list_length
    If Not (active_status_array.Contains(VA_Full.Range("active_status_list").item(i).Value)) Then
         active_status_array.Add (VA_Full.Range("active_status_list").item(i).Value)
    End If
    If Not (passive_status_array.Contains(VA_Full.Range("passive_status_list").item(i).Value)) Then
        passive_status_array.Add (VA_Full.Range("passive_status_list").item(i).Value)
    End If
    If Not (indicator_array.Contains(VA_Full.Range("indicator_list").item(i).Value)) Then
        indicator_array.Add (VA_Full.Range("indicator_list").item(i).Value)
    End If
Next

'Store array options in comboboxes
'active
For i = 1 To active_status_array.Count - 1
    active_status_cb.AddItem (active_status_array.item(i))
Next
'passive
For i = 1 To passive_status_array.Count - 1
    passive_status_cb.AddItem (passive_status_array.item(i))
Next
'indicator
For i = 1 To indicator_array.Count - 1
    indicator_cb.AddItem (indicator_array.item(i))
Next

End Sub
