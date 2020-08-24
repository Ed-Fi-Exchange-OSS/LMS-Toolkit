const fs = require('fs')
const converter = require('json-2-csv')

const ToCsv = (data, name) => {
  const json2csvCallback = (err, csv) => {
    if (err) throw err

    fs.writeFile(`${name}.csv`, csv, 'utf8', fsErr =>  {
      if (fsErr)
        console.log('Some error occured - file either not saved or corrupted file saved.')
      else
        console.log(`The file has been generated => ${name}.csv`)
    })
  }
  converter.json2csv(data, json2csvCallback);

}

exports.ToCsv = ToCsv
