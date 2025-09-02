<h1 align = "center">
Embracing Imperfection: Simulating Students with Diverse Cognitive Levels Using LLM-based Agents
</h1>
<div align='center'>
  <p style="margin:3px 0;">
    Tao Wu<sup>1</sup>, Jingyuan Chen<sup>1,&dagger;</sup>, Wang Lin<sup>1</sup>, Mengze Li<sup>2</sup>, Yumeng Zhu<sup>1</sup>, Ang Li<sup>1</sup>, Kun Kuang<sup>1</sup>, Fei Wu<sup>1,&dagger;</sup></p>
  <p style="margin:3px 0;">
  <sup>1</sup> Zhejiang University  &nbsp;&nbsp;&nbsp;
    <sup>2</sup> Hong Kong University of Science and Technology</p>
  <p style="margin:3px 0;">
    <sup>&dagger;</sup>Corresponding Authors</p>
  <p style="margin:3px 0;">
    <b>ACL 2025 Oral</b></p>
  <a href='https://arxiv.org/abs/2505.19997'><img src='https://img.shields.io/badge/Paper-Arxiv-red'></a> 
</div>



## Getting Started

**1. Installation**

You can follow the installation of [nano-graphrag](https://github.com/gusye1234/nano-graphrag):

```bash
# clone this repo first
cd student_sim
pip install -e .
```

**2. Prepare your API key**

We recommend setting the API keys in the environment variables:

```
export OPENAI_API_KEY=your key
```

Or you can directly modify in the code:

[src/nano_graphrag/_llm.py](src/nano_graphrag/_llm.py#L24)

[src/utils.py](src/utils.py#L17)

You can use your own model with the corresponding API key and URL in the OpenAI API form.

**3. Prepare the data**

Unfortunately, due to intellectual property constraints imposed by the PTA platform, the problem stem in the dataset is subject to copyright, and we are therefore unable to release the dataset publicly. We sincerely apologize for this inconvenience.

However, we have constructed two small-scale datasets, **Java_5** and **C++_5**, based on the publicly available CodeNet dataset. Aside from the source and programming language differences, these datasets share the same structure and characteristics as Student_100. Although the scale is limited—as they were built during the rebuttal phase—we hope they may still be of some help. 

Here is the dataset link: 

* [Google Drive](https://drive.google.com/drive/folders/1u1yiZmzXcck0BgjLuNBKtVeJ6imP7ray?usp=sharing)

You may also consider constructing additional datasets from sources like [CodeNet](https://github.com/IBM/Project_CodeNet) or other open programming platforms following a similar methodology.

After downloading the dataset, put them in a new folder `dataset`.

**4. Start Running**

```
python main.py
```



## Acknowledgment

This project is build upon [nano-graphrag](https://github.com/gusye1234/nano-graphrag) and partialy inspired by [Super_MARIO](https://github.com/MARIO-Math-Reasoning/Super_MARIO). We sincerely thank them for their pioneering exploration and contributions.



## Citation

If you found this work useful, please consider giving this repository a star and citing our paper as followed:

```
@inproceedings{studentsim,
  author       = {Tao Wu and
                  Jingyuan Chen and
                  Wang Lin and
                  Mengze Li and
                  Yumeng Zhu and
                  Ang Li and
                  Kun Kuang and
                  Fei Wu},
  editor       = {Wanxiang Che and
                  Joyce Nabende and
                  Ekaterina Shutova and
                  Mohammad Taher Pilehvar},
  title        = {Embracing Imperfection: Simulating Students with Diverse Cognitive
                  Levels Using LLM-based Agents},
  booktitle    = {Proceedings of the 63rd Annual Meeting of the Association for Computational
                  Linguistics (Volume 1: Long Papers), {ACL} 2025, Vienna, Austria,
                  July 27 - August 1, 2025},
  pages        = {9887--9908},
  publisher    = {Association for Computational Linguistics},
  year         = {2025},
  url          = {https://aclanthology.org/2025.acl-long.488/},
  timestamp    = {Thu, 24 Jul 2025 21:25:39 +0200},
  biburl       = {https://dblp.org/rec/conf/acl/WuCLLZLKW25.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

