# D6.5

## Рассылка
Что бы реализовать рассылку у модели Category была добавлена связь ManyToMany с моделью User,
таким образом у одного Post может быть много Category у которой в свою очередь может быть много
User в подпищиках.
Проблема в том что сигнал post_save не может работать со связями ManyToMany, поэтому рассылка была
реализована перегрузкой метода post у PostCreateView. Поэтому в данной работе мне не удалось
продемонстрировать применение сигналов, несмотря на то, что тема была мной изучена.