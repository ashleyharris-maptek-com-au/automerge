
"""
Represents a chunk of code that was commented out being renabled.
"""



import re
import itertools
import difflib
import LandmarkLib
import os

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

class Uncommented:
  def __init__(self) -> None:
    self.codeRegionsToUncomment = []

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  lineToLineMap, halfWayLines = LineToLineMapAndHalwayMap(oldLines, newLines)

  # We need to consider cases like
  # // blah-> blah(
  # //   blah)
  #
  #    ->
  #
  # blah->blah(blah)
  #
  # As it's quite common for commenting chunks of code to increase the column witdth,
  # requiring a re-wrap of the code. Code could also be uncommmented and changed - 
  # especially if code was commented out for having a bug, and then uncommented with
  # a fix in the same commit.

  commentRemoved = [False] * len(newLines)
    
  for oL, nL, index in zip(halfWayLines, newLines, range(len(newLines))):
    nLs = nL.strip()
    oLs = oL.strip()
    
    oLss = oLs.removeprefix("//")

    if oLss != oLs:
      oLsss = oLss.strip()
      commentRemoved[index] = oLsss == nLs



  qwe = ""


if __name__ == '__main__':
  Process("""
    Syncronise();
  }
  //{
  //  // Background pick object pass.
  //  mySolidColourBackgroundPickFramebufferPtr =
  //    myWindowRenderer->CreateFramebuffer();
  //  mySolidColourBackgroundPickColourRenderbufferPtr =
  //    CreateRenderbuffer(reeE_InternalFormat::R32UI);
  //  mySolidColourBackgroundPickDepthAndStencilRenderbufferPtr =
  //    myWindowRenderer->CreateRenderbuffer(
  //      reeE_InternalFormat::Depth24_Stencil8);

  //  mySolidColourBackgroundPickFramebufferPtr->AttachRenderbuffer(
  //    mySolidColourBackgroundPickColourRenderbufferPtr,
  //    reeE_FramebufferAttachmentPoint::Colour_Attachment0);
  //  mySolidColourBackgroundPickFramebufferPtr->AttachRenderbuffer(
  //    mySolidColourBackgroundPickDepthAndStencilRenderbufferPtr,
  //    reeE_FramebufferAttachmentPoint::Depth_Stencil_Attachment);

  //  myBackgroundPickObjectPass = reeT_RenderPassPtr(new S_Resource(
  //    mySolidColourBackgroundPickFramebufferPtr)));
  //}
  """.strip(),"""
    Syncronise();
  }
  {
    // Background pick object pass.
    mySolidColourBackgroundPickFramebufferPtr =
      myWindowRenderer->CreateFramebuffer();
    mySolidColourBackgroundPickColourRenderbufferPtr =
      myWindowRenderer->CreateRenderbuffer(reeE_InternalFormat::R32UI);

    // mySolidColourBackgroundPickDepthAndStencilRenderbufferPtr =
    //   myWindowRenderer->CreateRenderbuffer(
    //     reeE_InternalFormat::Depth24_Stencil8);

    RenderBufferCreationImpl(24,8);

    mySolidColourBackgroundPickFramebufferPtr->AttachRenderbuffer(
      mySolidColourBackgroundPickColourRenderbufferPtr,
      reeE_FramebufferAttachmentPoint::Colour_Attachment0);
    mySolidColourBackgroundPickFramebufferPtr->AttachRenderbuffer(
      mySolidColourBackgroundPickDepthAndStencilRenderbufferPtr,
      reeE_FramebufferAttachmentPoint::
        Depth_Stencil_Attachment);

    myBackgroundPickObjectPass = reeT_RenderPassPtr(
      new T_SolidColourPickPass(reeN_DefaultPassPolicy::MakeResources(
        mySolidColourBackgroundPickFramebufferPtr)));
  }
  """.strip())
