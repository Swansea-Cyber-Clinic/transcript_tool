import re, sys, argparse

parser = argparse.ArgumentParser(description='Removes extraneous speaker statements from transcripts')

parser.add_argument(
  'InputPath',
  metavar='path',
  type=str,
  help='path to input file'
)

parser.add_argument(
  '-o',
  metavar='path',
  type=str,
  help='path to output file'
)

args = parser.parse_args()

input_path = args.InputPath

try:
  with open(input_path, 'r') as txt:
    lines = txt.readlines()
    lines = [line.rstrip() for line in lines] # convert string into an array of strings separated by newline characters
    lines = list(filter(lambda a: a != '', lines)) # recast into list with blank entries removed
  txt.close()
except OSError:
  print(f"Could not open file \"{input_path}\"")
  sys.exit()

prev = 'Participant -1'

for line in lines:
    if re.search('(?P<Timecode>(?P<Hours>[0-1][0-9]|2[0-3]):(?P<Minutes>[0-5][0-9]):(?P<Seconds>[0-5][0-9]))', line): #is a line that begins with a timecode in the form XX:XX:XX...
        try:
            candidate = re.search('(?P<Timecode>(?P<Hours>[0-1][0-9]|2[0-3]):(?P<Minutes>[0-5][0-9]):(?P<Seconds>[0-5][0-9]) (?P<Name>[\s\S]*))', line).group('Name') # get the speaker name after the timecode
            if candidate != prev:
                prev = candidate
            else:
                lines.remove(line) # remove duplicate entry
        except AttributeError: # if name is blank for whatever reason
            pass

for line in lines:
    idx = lines.index(line)
    if re.search('(?P<Timecode>(?P<Hours>[0-1][0-9]|2[0-3]):(?P<Minutes>[0-5][0-9]):(?P<Seconds>[0-5][0-9]))', line): #is a timecode
        lines[idx] = lines[idx] + '\n'
        lines[idx-1] = lines[idx-1] + '\n'
    else:
        lines[idx] = lines[idx] + ' '

output_path = 'corrected_transcript.txt'
if args.o:
  output_path = args.o

transcript = ''.join(lines)
tx_file = open(output_path, 'w')
tx_file.write(transcript)
tx_file.close()