import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => new _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Container(
          color: Colors.white,
          // ignore: prefer_const_constructors
          margin: EdgeInsets.fromLTRB(0, 10, 0, 0),
          child: Home()),
    );
  }
}

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class Data {
  Map fetched_data = {
    "data": [
      {"id": 111, "name": "abc"},
      {"id": 222, "name": "pqr"},
      {"id": 333, "name": "abc"}
    ]
  };
  List _data = [];

//function to fetch the data

  Data() {
    _data = fetched_data["data"];
  }

  int getId(int index) {
    return _data[index]["id"];
  }

  String getName(int index) {
    return _data[index]["name"];
  }

  int getLength() {
    return _data.length;
  }
}

class _HomeState extends State<Home> {
  Data _data = new Data();

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: CupertinoNavigationBar(
            middle: Text('Race Manager'), backgroundColor: Colors.white),
        backgroundColor: Colors.white,
        body: Stack(
          children: [
            CupertinoSearchTextField(
              onChanged: (value) {},
              onSubmitted: (value) {},
              autocorrect: true,
              borderRadius: BorderRadius.circular(15.0),
            ),
            ListView.builder(
              padding: const EdgeInsets.fromLTRB(5.5, 35, 5.5, 5.5),
              itemCount: _data.getLength(),
              itemBuilder: _itemBuilder,
            )
          ],
        ),
      ),
    );
  }

  Widget _itemBuilder(BuildContext context, int index) {
    return InkWell(
        child: Container(
          height: 100,
          child: Card(
            shadowColor: Colors.blue[600],
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15.0)),
            child: InkWell(
              splashColor: Colors.blue.withAlpha(100),
              borderRadius: BorderRadius.circular(15.0),
              radius: 15.0,
              child: SizedBox(
                width: 300,
                height: 100,
                child: Center(
                  child: Text(
                    "${_data.getName(index)}",
                    style: TextStyle(
                      fontWeight: FontWeight.w500,
                      color: Colors.lightBlue[400],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
        onTap: () => {testAlert(context)});
  }

  void testAlert(BuildContext context) {
    var alert = AlertDialog(
      title: Text("Test"),
      content: Text("Done..!"),
    );

    showDialog(
        context: context,
        builder: (BuildContext context) {
          return alert;
        });
  }
}
