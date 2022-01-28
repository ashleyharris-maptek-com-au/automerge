from Merge import Merge
import MergeSimplifiers
import MergeStrategies
import itertools

def SolveMerge(m : Merge):
  
  merge = m
  while True:
    anyChange = False
    for ms in MergeSimplifiers.allMergeSimplifiers:
      m2 = ms(merge)
      if m2:
        merge = m2
        anyChange = True
    if anyChange == False: break

  allResults = {}  
  for solve in MergeStrategies.allStrategies:
    results = solve(merge)
    if results is not None:
      for k,v in results.items():
        if k in allResults: allResults[k] += v
        else: allResults[k] = v

  if len(allResults) == 0:
    return None

  q = max(allResults, key=allResults.get)

  if not q.endswith("\n"): q += "\n"

  return merge.prefix + q + merge.suffix


m = Merge()
m.fromString("""
<<<<<<< HEAD
#pragma once
///////////////////////////////////////////////////////////////////////////////
//
// Describes a texture binding point - a placeholder in a pipeline
// that specifies something like "All renderables added will have a 2D
// texture of RGBA 32-bit colour", without having to specify the actual
// texture.
//
// This allows multiple textured objects to be batched together on rendering
// engines like Vulkan and DirectX 12.
//
// Created on: 28 Nov 2021     Authors: Ashley Harris
//
// (C) Copyright 2005, Maptek Pty Ltd.  All rights reserved
//
///////////////////////////////////////////////////////////////////////////////

#include "Factory.H"

#include "mdf/shader/Program.H"

#include <variant>

namespace mdf
{
  using reeF_TexturePerformanceHint =
    reeN_Cobalt::ITextureBuffer::PerformanceHint;

  using reeT_TextureAndSamplerTypedPair = std::variant<
    std::pair<reeN_Cobalt::ITextureBuffer1D*, reeN_Cobalt::ITextureSampler1D*>,
    std::pair<reeN_Cobalt::ITextureBuffer2D*, reeN_Cobalt::ITextureSampler2D*>,
    std::pair<reeN_Cobalt::ITextureBuffer3D*, reeN_Cobalt::ITextureSampler3D*>,
    std::pair<reeN_Cobalt::ITextureBuffer1DArray*,
              reeN_Cobalt::ITextureSampler1DArray*>,
    std::pair<reeN_Cobalt::ITextureBuffer2DArray*,
              reeN_Cobalt::ITextureSampler2DArray*>>;

  struct reeS_TextureBindingDescription
  {
    Tbool isImageSizeFixed = true;
    Tbool isEverSampled = true;

    // Few other things may go here...
    // Tbool isDemandPagedPopulated = false;
    // Tbool isMipMapped = false;
    // Sampler wrap and border modes.

    shadE_DataDescriptor myDescriptor =
      shadE_DataDescriptor::DiffuseMapTexture;

    reeF_TexturePerformanceHint myGpuAccess =
      reeF_TexturePerformanceHint::WriteNever |
      reeF_TexturePerformanceHint::ReadOften;

    reeF_TexturePerformanceHint myCpuAccess =
      reeF_TexturePerformanceHint::WriteRarely |
      reeF_TexturePerformanceHint::ReadNever;

    // How large the images can be (sizeFixed == false) or are.
    Tuvec3 mySampledMaxDimensions = {1, 1, 1};
    Tint32u myArrayMaxElements = 1;

    Tbool operator==(const reeS_TextureBindingDescription& B) const
    {
      return true; // Just waiting until <=> works really.
    }
  };
}
||||||| merged common ancestors
=======
#pragma once
///////////////////////////////////////////////////////////////////////////////
//
// Describes a texture binding point - a placeholder in a pipeline
// that specifies something like "All renderables added will have a 2D
// texture of RGBA 32-bit colour", without having to specify the actual
// texture.
//
// This allows multiple textured objects to be batched together on rendering
// engines like Vulkan and DirectX 12.
//
// Created on: 28 Nov 2021     Authors: Ashley Harris
//
// (C) Copyright 2022, Maptek Pty Ltd. All Rights Reserved
//
///////////////////////////////////////////////////////////////////////////////

#include "Factory.H"

#include "mdf/shader/Program.H"

#include <variant>

namespace mdf
{
  using reeF_TexturePerformanceHint =
    reeN_Cobalt::ITextureBuffer::PerformanceHint;

  using reeT_TextureAndSamplerTypedPair = std::variant<
    std::pair<reeN_Cobalt::ITextureBuffer1D*, reeN_Cobalt::ITextureSampler1D*>,
    std::pair<reeN_Cobalt::ITextureBuffer2D*, reeN_Cobalt::ITextureSampler2D*>,
    std::pair<reeN_Cobalt::ITextureBuffer3D*, reeN_Cobalt::ITextureSampler3D*>,
    std::pair<reeN_Cobalt::ITextureBuffer1DArray*,
              reeN_Cobalt::ITextureSampler1DArray*>,
    std::pair<reeN_Cobalt::ITextureBuffer2DArray*,
              reeN_Cobalt::ITextureSampler2DArray*>>;

  struct reeS_TextureBindingDescription
  {
    Tbool isImageSizeFixed = true;
    Tbool isEverSampled = true;

    // Few other things may go here...
    // Tbool isDemandPagedPopulated = false;
    // Tbool isMipMapped = false;
    // Sampler wrap and border modes.

    shadE_DataDescriptor myDescriptor =
      shadE_DataDescriptor::DiffuseMapTexture;

    reeF_TexturePerformanceHint myGpuAccess =
      reeF_TexturePerformanceHint::WriteNever |
      reeF_TexturePerformanceHint::ReadOften;

    reeF_TexturePerformanceHint myCpuAccess =
      reeF_TexturePerformanceHint::WriteRarely |
      reeF_TexturePerformanceHint::ReadNever;

    // How large the images can be (sizeFixed == false) or are.
    Tuvec3 mySampledMaxDimensions = {1, 1, 1};
    Tint32u myArrayMaxElements = 1;

    Tbool operator==(const reeS_TextureBindingDescription& B) const
    {
      return true; // Just waiting until <=> works really.
    }
  };
}
>>>>>>> 01621e0e98cc5f37df414ff8d1707ef856b210bd

""")

#r = SolveMerge(m)

#print(r)