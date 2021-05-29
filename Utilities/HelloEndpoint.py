{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7dac22b9",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install Flask==2.0.1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d19b1dcb",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__' (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on all addresses.\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      " * Running on http://10.142.0.3:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [29/May/2021 04:18:02] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [29/May/2021 04:18:04] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [29/May/2021 04:18:04] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [29/May/2021 04:18:04] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [29/May/2021 04:18:04] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [29/May/2021 04:18:04] \"GET / HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route('/')\n",
    "def hello_world():\n",
    "    return {\"Hello Feli\": \"Fight or NonFight?\"}\n",
    "\n",
    "app.run(host=\"0.0.0.0\") "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e5dd4944",
   "metadata": {},
   "outputs": [],
   "source": [
    "#http://35.231.229.100:5000/"
   ]
  }
 ],
 "metadata": {
  "environment": {
   "name": "tf2-gpu.2-5.m70",
   "type": "gcloud",
   "uri": "gcr.io/deeplearning-platform-release/tf2-gpu.2-5:m70"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
