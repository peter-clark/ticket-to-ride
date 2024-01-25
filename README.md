# ticket-to-ride optimzer
Representation of Ticket to Ride: Rails and Sails board game. The purpose of this repository is to crunch some numbers about optimization in Ticket to Ride.

### Example:
All Routes between (New York City -> Jakarta) with length<=16:

```
Shortest Route:
[13] (~)09/04(=) >> NYC === LOS ~~~ HON ~~~ PTM ~~~ DAR ~~~ JAK
All Routes:
[13] (~)09/04(=) >> NYC === LOS ~~~ HON ~~~ PTM ~~~ DAR ~~~ JAK
[14] (~)10/04(=) >> NYC === LOS ~~~ HON ~~~ MAN ~~~ JAK
[14] (~)09/05(=) >> NYC === WIN === VAN === LOS ~~~ HON ~~~ PTM ~~~ DAR ~~~ JAK
[14] (~)10/04(=) >> NYC === WIN === VAN ~~~ TOK ~~~ MAN ~~~ JAK
[14] (~)09/05(=) >> NYC === WIN === LOS ~~~ HON ~~~ PTM ~~~ DAR ~~~ JAK
[15] (~)10/05(=) >> NYC === LOS === VAN ~~~ TOK ~~~ MAN ~~~ JAK
[15] (~)11/04(=) >> NYC === LOS ~~~ TOK ~~~ MAN ~~~ JAK
[15] (~)10/05(=) >> NYC === WIN === VAN === LOS ~~~ HON ~~~ MAN ~~~ JAK
[15] (~)10/05(=) >> NYC === WIN === LOS ~~~ HON ~~~ MAN ~~~ JAK
[16] (~)11/05(=) >> NYC === LOS ~~~ HON ~~~ MAN ~~~ HKG === BKK ~~~ JAK
[16] (~)12/04(=) >> NYC === LOS ~~~ HON ~~~ MAN ~~~ BKK ~~~ JAK
[16] (~)12/04(=) >> NYC === LOS ~~~ HON ~~~ TOK ~~~ MAN ~~~ JAK
[16] (~)10/06(=) >> NYC === LOS ~~~ HON ~~~ PTM ~~~ DAR === PER ~~~ JAK
[16] (~)11/05(=) >> NYC === WIN === VAN === LOS ~~~ TOK ~~~ MAN ~~~ JAK
[16] (~)11/05(=) >> NYC === WIN === VAN ~~~ TOK ~~~ HKG === BKK ~~~ JAK
[16] (~)12/04(=) >> NYC === WIN === VAN ~~~ TOK ~~~ HKG ~~~ MAN ~~~ JAK
[16] (~)11/05(=) >> NYC === WIN === VAN ~~~ TOK ~~~ MAN ~~~ HKG === BKK ~~~ JAK
[16] (~)12/04(=) >> NYC === WIN === VAN ~~~ TOK ~~~ MAN ~~~ BKK ~~~ JAK
[16] (~)10/06(=) >> NYC === WIN === LOS === VAN ~~~ TOK ~~~ MAN ~~~ JAK
[16] (~)11/05(=) >> NYC === WIN === LOS ~~~ TOK ~~~ MAN ~~~ JAK
```