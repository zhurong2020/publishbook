# 单词数据结构说明

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 唯一标识符 |
| word | string | 是 | 单词 |
| phonetic_uk | string | 是 | 英式音标 |
| phonetic_us | string | 是 | 美式音标 |
| part_of_speech | array | 是 | 词性列表 |
| definitions.chinese | array | 是 | 中文释义列表 |
| definitions.english | array | 是 | 英文释义列表 |
| examples | array | 是 | 例句列表（至少2个） |
| collocations | array | 是 | 常用搭配 |
| derivatives | array | 否 | 派生词 |
| synonyms | array | 否 | 同义词 |
| antonyms | array | 否 | 反义词 |
| memory_tip | string | 否 | 记忆技巧 |
| confused_words | array | 否 | 易混词 |
| level | string | 是 | CEFR等级 (A1-C2) |
| frequency | string | 是 | 词频等级 |
| chapter | number | 是 | 所属章节 |
| section | string | 是 | 所属小节 |
| tags | array | 否 | 标签 |

## 词性代码

- noun: 名词
- verb: 动词
- adjective: 形容词
- adverb: 副词
- pronoun: 代词
- preposition: 介词
- conjunction: 连词
- interjection: 感叹词

## CEFR 等级说明

- **A1** (入门级): 最基础的日常词汇
- **A2** (初级): 基础交流词汇
- **B1** (中级): 日常交流和工作词汇
- **B2** (中高级): 较复杂的交流词汇
- **C1** (高级): 学术和专业词汇
- **C2** (精通级): 高级学术和文学词汇

## 词频等级

- **high**: 高频词（日常对话和写作中经常使用）
- **medium**: 中频词（一般阅读中常见）
- **low**: 低频词（专业或正式场合使用）
