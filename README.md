# remo

- Nature Remo Cloud API を利用して Remo の温度センサーから温度情報を取得する
- 取得した温度情報を Google Cloud API を利用して Google Sheets に記録する

## Setup

- [Nature Developer Page](https://developer.nature.global/) に従って Nature Remo Cloud API トークンを取得し、 `.env` を編集する
- [Python で Google Sheets を編集する方法](https://www.twilio.com/blog/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python-jp) に従って `client-secret.json` を取得し、 `.env` を編集する

## Execution

```shell
$ poetry install
$ poetry run invoke run
```

## Resources

- [Nature Developer Page](https://developer.nature.global/)
- [API 仕様 [CLOUD API]](https://swagger.nature.global/)
- [Python で Google Sheets を編集する方法](https://www.twilio.com/blog/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python-jp)
- [Examples of gspread Usage](https://docs.gspread.org/en/latest/user-guide.html)
