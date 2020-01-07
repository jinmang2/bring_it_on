- [argparse 자습서](https://docs.python.org/ko/3/howto/argparse.html)
```python
# test.py
import argparse, json, os

def main(args):
    print(args.all)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Download Kinetics videos in the mp4 format.")

    parser.add_argument("--categories", nargs="+", help="categories to download")
    parser.add_argument("--classes", nargs="+", help="classes to download")
    parser.add_argument("--all", action="store_true", help="download the whole dataset")
    parser.add_argument("--test", action="store_true", help="download the test set")

    parser.add_argument("--num-workers", type=int, default=1, help="number of downloader processes")
    parser.add_argument("--failed-log", default="dataset/failed.txt", help="where to save list of failed videos")
    parser.add_argument("--compress", default=False, action="store_true", help="compress videos using gzip (not recommended)")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="print additional info")
    parser.add_argument("-s", "--skip", default=False, action="store_true", help="skip classes that already have folders")
    parser.add_argument("-l", "--log-file", help="log file for youtube-dl (the library used to download YouTube videos)")
    
    parsed = parser.parse_args()
    main(parsed)
```

In python shell,
```
(basic) E:\kinetics700\kinetics-downloader>python test.py
False

(basic) E:\kinetics700\kinetics-downloader>python test.py --all
True
```
