# Who's this for?
This writeup is for someone that has an ETL with a busted blockchain.db or busted ledger, but their postgres db is intact. 

# I broke my ETL what do I do? 

1. Don't panic it's mostly fixable. 
2. Take a deep breath

## Get the height of the postgres db

1. Check the api for the height of the db or go directly into the DB and figure out the highest blocks in blocks table
   - Here: `https://<api>/v1/blocks/height`
2. Find a good snapshot from Helium that is below the height in the DB. 
   - `https://api.helium.io/v1/snapshots`
>  You should be able to curl any anyshot here just use the block height shown. 

>  MAKE SURE THE BLOCK HEIGHT IS BELOW THE HEIGHT OF THE DB.
>  this can't be stressed enough.
```json
  {"data":[{"snapshot_hash":"V1aV6g3UxPo4OaBMlsaYhgS9EW3VYrYGwnc7f3jb5Ww","block":975601},
  {"snapshot_hash":"yf9By9NjzBY4y4MKxAEH4BvlWUtRWSpdA5B-8SAvxyk","block":974881},
  {"snapshot_hash":"lVChIDC_4qjeNDMF9VCset4GR2bwDtqxJKIdrIYbTLc","block":972721}
  ,{"snapshot_hash":"Is6a-RIu4-XAZGVm82t3zznbah7nHVLd6nS9QAFGN48","block":959041},
  {"snapshot_hash":"paHCvvgzC1Z0L0NL8XwY6Ib6t9xNni6ojzi48sovq3U","block":958321},
  {"snapshot_hash":"czfd3gZ9ZKjk9hPBnkRTRBjqDKXoo3UyhW1YukWvW6g","block":956881},
  {"snapshot_hash":"2cyUzrbpj5hZSSYXjwGlfDmwD5K4buIMNtVjBXemdxc","block":953281},
  {"snapshot_hash":"CGDVMBva1G0UKPshGS2_zk8N1Uak591CSrT4Hv0JhW4","block":952561},
```
3. Download this snapshot that you find with the appropriate block height from above. .
   - `bash curl -O https://snapshots.helium.wtf/mainnet/snap-<height>`

## Misconceptions I made 
I was living under the premise that you need a whole copy of the blockchain to run ETL. You really only need a whole copy of the blockchain if you don't have a decent current ETL database in postgres.  This is not the case. You just need a snapshot that starts below the height of the ETL postgres DB and shazam. 

1. Take very regular backups of postgres.
2. Make snapshots for yourself. 
3. Don't sweat blockchain db as hard as I did. Just take great care of your ETL DB in postgres and start from snapshots. 


## Ok I heard you, what's next. 
If you are like me and completely jacked up the blockchain.db and ledger.db, rename those directories. Don't just delete them silly goose. 

1. etl stop 
2. killall epmd (for good luck)
3. mv blockchain.db blockchain.db.densone
4. mv ledger.db ledger.db.densone
5. etl start 
6. etl repair sync_pause 
7. etl repair sync_cancel 
8. etl snapshot load /path/to/the/helium/snapshot
9. etl repair sync_resume
10. cross your fingers and it should do the right things. 

## In conclusion 

1. Take great care of postgres db 
2. Worry less about blockchain.db if you corrupted it. You don't need the whole thing unless you are starting with a fresh postgres db, and in that case. I hope you have a backup somewhere. 

