# page_turner

This repo started as an automatic page-turner for pianists, but now I just put music-related things in here. It includes:
1. an automatic page-turner (useful for performing),
2. a stave-finder for segmenting score images (useful for producing score videos),
3. a random chord-sequence generator (useful for composing).

## How to use the page turner
Instructions: 

0. Download the facial landmarks detector and place in root folder. Install all dependencies (imutils, opencv-python, numpy, dlib, keyboard, shlex).
1. Call the script in Terminal ("python3 turn_pages.py").
2. Open your music score in Adobe Acrobat. Alternatively, you can also let the program open scores for you using set_up_score().
3. Turn your head slightly for about a second in the desired direction, and page will follow!
4. The page turner will continue turning pages. To exit, quit Adobe and terminate the process in shell.

The facial landmarks detector can be found at https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat

P.S. Yes, I am aware that Piascore exists, but it is only available on iPad and cell phones, not laptops, and reading from these smaller devices hurts my eyes.

P.P.S. Piascore uses winks instead of head tilts, but I have monovision and would like to avoid using eye signals if at all possible.
