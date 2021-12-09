from Merge import Merge
import DiffSolver

def Solve(m : Merge):
  """
  Not working? The merge may be decorated - or the decoration could
  be changed as part of the diff.

  The most common decoration is comments or end of line escapes:

  #DEFINE Impl() void Function(                 \ 
  <<<<<<<<                                                        
  vgC_Stream *StreamWorldSpace,      \ 
  vgC_Stream *StreamScreenSpace) {   \ 
  ||||||||                                                        
  vgC_Stream* StreamWorldSpace,           \ 
  vgC_Stream* StreamScreenSpace) {        \ 
  ========                                                        
  vgC_Stream* StreamWorldSpace,   \ 
  vgC_Stream* StreamScreenSpace)  \ 
  {                               \ 
  >>>>>>>>

  By detecting the decoration "all lines end in \ ", that information
  can be extracted to be applied later, the merge recursed, and the 
  following merge is now trivial:

  <<<<<<<<                                                        
  vgC_Stream *StreamWorldSpace,                                  
  vgC_Stream *StreamScreenSpace) {                               
  ||||||||                                                        
  vgC_Stream* StreamWorldSpace,                                  
  vgC_Stream* StreamScreenSpace) {                               
  ========                                                        
  vgC_Stream* StreamWorldSpace,   
  vgC_Stream* StreamScreenSpace)  
  {                               
  >>>>>>>>

  (It's identical sans whitespace). That can be solved and then redecorated.

  """
