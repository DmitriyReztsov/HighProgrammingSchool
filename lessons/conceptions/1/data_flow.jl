#=
Что произойдет, если операция попытается использовать переменную, которая еще не определена
(идентификатор не связан с конкретным значением)? Даже с эстетической точки зрения было бы неплохо,
если бы операция просто подождала, когда в эту переменную загрузится некоторое первичное значение.
Например, переменную инициализирует какая-нибудь другая нить, и затем данная операция сможет продолжить работу.
Такая парадигма называется dataflow (поток данных).

Thread 1:
global b = false
global a = rand()
global b = true

Thread 2:
while !b; end
use(a)

Имеется макро @isdefined, которое проверяет, определена ли некоторая переменная x: 
Thread 3:
while ! @isdefined(a); end
use(a)

В целом, парадигма Dataflow отличается, во-первых, независимыми корректными вычислениями --
независимо от того, как они распределяются по параллельным процессам.
Например, имеются три функции, первая из которых возводит глобальную переменную X в квадрат,
как только она будет определена. Вторая функция задаёт переменной X значение 9, и третья функция
выполняет задержку работы всей программы на 10 секунд.
В каком бы порядке мы не стали вызывать эти функции, как бы мы не распределили их по нитям,
в парадигме Dataflow итог всегда будет один и тот же: программа замирает на 10 секунд и выдаёт значение 81.

И во-вторых, сами вычисления скромны и терпеливы: они не посылают никаких сигналов, а просто ждут,
когда активизируются нужные им данные.

Добавление нитей и временных задержек в программу может кардинально изменить форму её работы,
но до тех пор, пока одни и те же операции вызываются с одними и теми же аргументами, результаты программы
всегда будут одними и теми же. Это ключевое свойство dataflow-параллелизма.
Поэтому данная парадигма предоставляет множество преимуществ параллелизма без излишних сложностей, обычно ему присущих. 
=#

for i = 1:5
    if @isdefined a
        print(a)
    end
    a = i
    sleep(1)
    print("--")
end
