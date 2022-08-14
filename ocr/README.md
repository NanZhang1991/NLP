## pytesseract 
pytesseract 的功能比tesserocr 强大，且版本更新较快，但pytesseract 的使用需要tesseract的支持 请注意pytesseract 版本对应的tesseract版本
例如pytesseract 0.3.7对应tesseract4.0 以上版本
tesseract官网安装指导
https://github.com/tesseract-ocr/tesseract
https://tesseract-ocr.github.io/tessdoc/Home.html
官网也是ubuntu 安装
https://launchpad.net/~alex-p/+archive/ubuntu/tesseract-ocr-devel
**Adding this PPA to your system**
```bash
add-apt-repository ppa:alex-p/tesseract-ocr-devel
apt-get update
apt-get install tesseract-ocr
tesseract --version
```
## paddleocr
官网连接 https://github.com/PaddlePaddle</br>
https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.4/ppstructure/docs/quickstart.md</br>
paddleocr 需要先运行.py的脚本下载相关模型</br>
paddlepaddle-gpu 版本注意支持的cuda版本

```bash
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
pip install -U https://paddleocr.bj.bcebos.com/whl/layoutparser-0.0.0-py3-none-any.
pip install "paddleocr>=2.2"
```
