<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This amazing python project combines some random open source library called pydub and the awesome GUI making features provided by PyQt6 in order to create a human-friendly audio editor. Software implements never seen before features like adding gain, cutting and merging :O, and adding fade effects. It even allows to play the audio WITHOUT having to export it! WOW!. It handles uncounted amount of file formats, literally (.mp3 and .wav work). Bascially, an amazing piece of software made with dedication, time and will to pass the subject :).



### Built With

* pydub  (https://github.com/jiaaro/pydub)
* PyQt6  (https://pypi.org/project/PyQt6/)
* FFMPEG (https://ffmpeg.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

* Install python
* Install FFMPEG
* Run GUI.py with python

Code is split into 2 files:
GUI.py contains all the PyQt features (frontend),
AudioManager.py contains all the pydub features (backend).

Simplest way of adding functionality:
1. Create a backend method in AudioManager.py, which you can pass arguments to, do the logic in that method.
2. Build a frontend consisting of input fields and an apply button, which invokes above backend method.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
