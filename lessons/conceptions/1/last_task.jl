#======= 38.

Имеется функция, для которой возникает race condition:

function mycount(n)
    c = 0
    for i in 1:n
        c += i
    end
    return c
end

Если для изменения глобальной переменной "с" будут использованы атомарные операции, поможет ли это избавиться от проблемы конкуренции?

да

нет <---

======= 39.

Если требуется просуммировать массив в параллельном режиме, то, с учётом предыдущей проблемы, начинающие нередко делают так: создают дополнительный глобальный массив или словарь, где для каждого потока создают свой счётчик, в который заносится сумма некоторого поддиапазона массива, заданного соответствующему потоку , и потом в итоге суммируются все эти счётчики.
Но в такой ситуации нередко возникает негативный эффект false sharing, связанный с резким увеличением накладных расходов на синхронизацию блоков кэш-памяти, к которым обращается несколько потоков.
Сегодня фактически все многоядерные процессоры поддерживают протокол cache coherence (своеобразная синхронизация ячеек локальных кэшей). Но даёт ли этот протокол реальный эффект, ведь виртуальные машины наподобие JVM могут использовать собственные архитектуры поддержки параллельных вычислений?

скорее да

it depends <---

скорее нет

======= 40.

Требуют ли атомарные арифметические и подобные им операции больше или меньше ресурсов в сравнении с обычной арифметикой?

атомарные операции быстрее в сотни-тысячи раз

атомарные операции быстрее в десятки-сотни раз

атомарные операции такие же по быстродействию

атомарные операции медленнее в десятки-сотни раз

атомарные операции медленнее в сотни-тысячи раз

it depends <---

======= 41.

Имеется функция, заполняющая в параллельном режиме массив случайными значениями и вычисляющая его сумму:

function thread_test(v)
  Threads.@threads for i = 1:length(v)
      @inbounds v[i] = rand()
  end
  sum(v)
end

@inbounds -- это макро, отключающая проверки возможного выхода индекса за пределы массива, так как в данном случае индекс будет всегда лежать в его границах.

Может ли при выполнении такого кода возникнуть race condition?

да <---

нет
=#