# ticket-to-ride optimzer
Representation of Ticket to Ride: Rails and Sails board game. The purpose of this repository is to crunch some numbers about optimization in Ticket to Ride.

### Example:
All Routes between (New York City -> Jakarta) with length<=16:
KEY: ```[~~#~~ : ship]  [==#== : train] [# : amt]```
```
Shortest Route:
[13] (~)09/04(=) >> NYC ==4== LOS ~~3~~ HON ~~3~~ PTM ~~1~~ DAR ~~2~~ JAK
All Routes:
[13] (~)09/04(=) >> NYC ==4== LOS ~~3~~ HON ~~3~~ PTM ~~1~~ DAR ~~2~~ JAK
[14] (~)10/04(=) >> NYC ==4== LOS ~~3~~ HON ~~5~~ MAN ~~2~~ JAK
[14] (~)09/05(=) >> NYC ==2== WIN ==2== VAN ==1== LOS ~~3~~ HON ~~3~~ PTM ~~1~~ DAR ~~2~~ JAK
[14] (~)10/04(=) >> NYC ==2== WIN ==2== VAN ~~6~~ TOK ~~2~~ MAN ~~2~~ JAK
[14] (~)09/05(=) >> NYC ==2== WIN ==3== LOS ~~3~~ HON ~~3~~ PTM ~~1~~ DAR ~~2~~ JAK
[15] (~)10/05(=) >> NYC ==4== LOS ==1== VAN ~~6~~ TOK ~~2~~ MAN ~~2~~ JAK
[15] (~)11/04(=) >> NYC ==4== LOS ~~7~~ TOK ~~2~~ MAN ~~2~~ JAK
[15] (~)10/05(=) >> NYC ==2== WIN ==2== VAN ==1== LOS ~~3~~ HON ~~5~~ MAN ~~2~~ JAK
[15] (~)10/05(=) >> NYC ==2== WIN ==3== LOS ~~3~~ HON ~~5~~ MAN ~~2~~ JAK
[16] (~)11/05(=) >> NYC ==4== LOS ~~3~~ HON ~~5~~ MAN ~~1~~ HKG ==1== BKK ~~2~~ JAK
[16] (~)12/04(=) >> NYC ==4== LOS ~~3~~ HON ~~5~~ MAN ~~2~~ BKK ~~2~~ JAK
[16] (~)12/04(=) >> NYC ==4== LOS ~~3~~ HON ~~5~~ TOK ~~2~~ MAN ~~2~~ JAK
[16] (~)10/06(=) >> NYC ==4== LOS ~~3~~ HON ~~3~~ PTM ~~1~~ DAR ==2== PER ~~3~~ JAK
[16] (~)11/05(=) >> NYC ==2== WIN ==2== VAN ==1== LOS ~~7~~ TOK ~~2~~ MAN ~~2~~ JAK
[16] (~)11/05(=) >> NYC ==2== WIN ==2== VAN ~~6~~ TOK ~~3~~ HKG ==1== BKK ~~2~~ JAK
[16] (~)12/04(=) >> NYC ==2== WIN ==2== VAN ~~6~~ TOK ~~3~~ HKG ~~1~~ MAN ~~2~~ JAK
[16] (~)11/05(=) >> NYC ==2== WIN ==2== VAN ~~6~~ TOK ~~2~~ MAN ~~1~~ HKG ==1== BKK ~~2~~ JAK
[16] (~)12/04(=) >> NYC ==2== WIN ==2== VAN ~~6~~ TOK ~~2~~ MAN ~~2~~ BKK ~~2~~ JAK
[16] (~)10/06(=) >> NYC ==2== WIN ==3== LOS ==1== VAN ~~6~~ TOK ~~2~~ MAN ~~2~~ JAK
[16] (~)11/05(=) >> NYC ==2== WIN ==3== LOS ~~7~~ TOK ~~2~~ MAN ~~2~~ JAK
```