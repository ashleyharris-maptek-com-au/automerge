from Merge import Merge
import DiffSolver
import os, sys, subprocess
import DiffCalcs.U as U
import random,re

repoBase = 'C:/AshDev/views/cmdf'
filePath = 'mdf/mdf/renderer/TextureBindingDescription.H'
gitPath = 'C:/cygwin64/bin/git'

def Solve(m : Merge):
  hash1 = m.actualHash
  hash2 = m.newHash

  if hash1 is None or hash1 == "": return None
  if hash2 is None or hash2 == "": return None

  oldcwd = os.getcwd()

  os.chdir(repoBase)

  hashes1 = subprocess.run(
    [gitPath, 'log', '--format=%H', '-4', '--no-merges', hash1, '--', filePath], 
    stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()

  hashes2 = subprocess.run(
    [gitPath, 'log', '--format=%H', '-4', '--no-merges', hash2, '--', filePath], 
    stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()

  allHashes = []
  allHashes.extend(hashes1)
  allHashes.extend(hashes2)

  allDiffChains = []

  for hash in allHashes:
    diff = subprocess.run(
      [gitPath, 'show', hash, '--pretty=format:%b', filePath], 
      stdout=subprocess.PIPE).stdout.decode("utf-8")

    if "\n+++ /dev/null" in diff or "\n--- /dev/null" in diff: continue

    if "<<<<<<" in diff: continue

    old = ""
    new = ""

    inHunk = False
    for l in diff.splitlines():
      if l.startswith("@@"):
        if inHunk:
          #Urgh two hunks.
          diffChain = DiffSolver.AllPossibleSolutions(old,new)
          allDiffChains.extend(diffChain)
          old = ""
          new = ""

        inHunk = True
        continue
      if inHunk and l[0] == ' ':
        old += l[1:]
        new += l[1:]
        old += "\n"
        new += "\n"
        continue
      if inHunk and l[0] == '+':
        new += l[1:]
        new += "\n"
        continue
      if inHunk and l[0] == '-':
        old += l[1:]
        old += "\n"
        continue

    diffChain = DiffSolver.AllPossibleSolutions(old,new)

    allDiffChains.extend(diffChain)

  os.chdir(oldcwd)

  if m.expected.strip() == "":
    # Two concurrent insertions

    left = m.actual
    right = m.new

    diffChains = allDiffChains

    while True:
      
      diffRatio = U.ratio(left,right)

      diffChainsCopy = diffChains
      anyChange = False

      for chain in diffChainsCopy:
        left2 = chain.applyTo(left)

        if left != left2:
          left2r = U.ratio(left2, right)

          if (left2r > diffRatio):
            diffRatio = left2r
            left = left2
            diffChains.remove(chain)
            anyChange = True
            break

        right2 = chain.applyTo(right)

        if right != right2:
          right2r = U.ratio(left, right2)

          if right2r > diffRatio:
            diffRatio = right2r
            right = right2
            diffChains.remove(chain)
            anyChange = True
            break

      if not anyChange: break

    if re.sub(r"\s","",left) == re.sub(r"\s","",right):
      # We've found an answer
      allResults = {}
      allResults[left] = 1
      if right in allResults: allResults[right] += 1
      else: allResults[right] = 1

      return allResults

  else:
    
    allResults = {}
    
    for attempt in range(10):
      random.shuffle(allDiffChains)

      text = m.expected

      for step in allDiffChains:
        text2 = step.applyTo(text)
        if text2 is None: continue
        if text2 == text: continue
        text = text2
      
      if text == m.expected: continue

      if text in allResults: allResults[text] += 1
      allResults[text] = 1
    return allResults