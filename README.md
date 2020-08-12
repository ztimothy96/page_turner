# page_turner

An automatic page turner! (Intended for pianists, but perhaps there are other use cases?)

Instructions: 

0. Download the facial landmarks detector and place in root folder. Install all dependencies (imutils, opencv-python, keyboard, shlex).
1. Call the script in Terminal ("python3 turn_pages.py"), 
2. Open your music score in Adobe Acrobat. Alternatively, you can also let the program open scores for you using set_up_score().
3. Turn your head slightly for about a second in the desired direction, and page will follow!
4. The page turner will continue turning pages. To exit, quit Adobe and terminate the process in shell.

The facial landmarks detector can be found at https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat

P.S. Yes, I am aware that Piascore exists, but it is only available on iPad and cell phones, not laptops, and reading from these smaller devices hurts my eyes.
P.P.S. Piascore uses winks instead of head tilts, but I have monovision and would like to avoid using eye signals if at all possible.
