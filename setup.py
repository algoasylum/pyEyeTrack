from distutils.core import setup

install_requires = []

with open('requirements.txt') as f:
    for line in f.readlines():
        req = line.strip()
        if not req or req.startswith('#') or '://' in req:
            continue
        install_requires.append(req)


setup(
  name = 'PyEyeTrack',         
  packages = ['PyEyeTrack'],   
  version = '0.3.1',      
  license='MIT',        
  description = """PyEyeTrack is a python-based pupil-tracking library. The library tracks eyes with the commodity webcam 
                and gives a real-time stream of eye coordinates. It provides the functionality of eye-tracking and 
                blink detection and encapsulates these in a generic interface that allows clients to use these 
                functionalities in a variety of use-cases.""",   
  authors = 'Kanchan Sarolkar, Kimaya Badhe, Neha Chaudhari, Samruddhi Kanhed and Shrirang Karandikar',                   
  author_email = 'pytracklibrary@gmail.com',      
  url = 'https://github.com/algoasylum/PyEyeTrack',  
  download_url = 'https://github.com/algoasylum/pyEyeTrack/archive/v_03_1.tar.gz',    
  keywords = ['Eye Tracking','blink detection','User Interface','Webcamera'],   
  install_requires=install_requires,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)