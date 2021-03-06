import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_app/services/requests.dart';

String image = '';
var flag = true;

class Results extends StatelessWidget {
  late String idRace;
  late String className;
  static String routeName = '/results';

  @override
  Widget build(BuildContext context) {
    var myArgument = (ModalRoute.of(context)?.settings.arguments) as List;
    this.idRace = myArgument[0];
    this.className = myArgument[1];
    return Scaffold(
      body: MyResultsPage(idRace, className),
    );
  }
}

class MyResultsPage extends StatefulWidget {
  late String idRace;
  late String className;

  MyResultsPage(toSet0, toSet1) {
    idRace = toSet0;
    className = toSet1;
  }

  @override
  _MyResultsPageState createState() => _MyResultsPageState(idRace, className);
}

class _MyResultsPageState extends State<MyResultsPage> {
  late String idRace;
  late String className;

  _MyResultsPageState(toSet0, toSet1) {
    this.idRace = toSet0;
    this.className = toSet1;
  }

  List items = [];
  ScrollController _scrollController = new ScrollController();
  bool isPerformingRequest = false;

  @override
  void initState() {
    super.initState();
    _getMoreData();
    _scrollController.addListener(() {
      if (_scrollController.position.pixels ==
          _scrollController.position.maxScrollExtent) {
        _getMoreData();
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  _getMoreData() async {
    if (!isPerformingRequest) {
      setState(() => isPerformingRequest = true);
      final List newEntries =
          await Request.getResultsOfRaceClass(idRace, className);
      /*if (newEntries.isEmpty) {
        double edge = 50.0;
        double offsetFromBottom = _scrollController.position.maxScrollExtent -
            _scrollController.position.pixels;
        if (offsetFromBottom < edge) {
          _scrollController.animateTo(
              _scrollController.offset - (edge - offsetFromBottom),
              duration: Duration(milliseconds: 100),
              curve: Curves.easeOut);
        }
      }*/
      setState(() {
        items.clear();
        items.addAll(newEntries);
        isPerformingRequest = false;
      });
    }
  }

  Widget _buildProgressIndicator() {
    double horSize = MediaQuery.of(context).size.width / 2;
    double verSize = MediaQuery.of(context).size.height / 2;
    return Padding(
      padding:
          EdgeInsets.symmetric(horizontal: horSize / 2, vertical: verSize / 2),
      child: Center(
        child: Opacity(
          opacity: _getOpacity(),
          child: CircularProgressIndicator(),
        ),
      ),
    );
  }

  double _getOpacity() {
    if (isPerformingRequest && flag) {
      flag = false;
      return 1.0;
    }
    return 0.0;
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: () => _getMoreData(),
      child: Scaffold(
        appBar: CupertinoNavigationBar(
          middle: Text(className),
        ),
        body: ListView.builder(
          itemCount: items.length + 1,
          itemBuilder: (context, index) {
            if (index >= items.length - 1) {
              return _buildProgressIndicator();
            } else {
              var toText = items[index];
              var id = toText['idPlayer'];
              var name = toText['name'];
              var surname = toText['surname'];
              return ListTile(
                title: Text(name + ' ' + surname),
                subtitle: Text(id),
                leading: Container(
                  height: 35.0,
                  width: 35.0,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.lightBlue,
                  ),
                  child: Center(
                    child: Text(
                      (index + 1).toString(),
                      style: TextStyle(fontSize: 22, color: Colors.white),
                    ),
                  ),
                ),
                onTap: () {},
              );
            }
          },
          controller: _scrollController,
        ),
        floatingActionButton: FloatingActionButton(
          child: Icon(Icons.dataset),
          onPressed: () async {
            await _dialogCall(
                context, await Request.getSplitTimesImage(idRace, className));
          },
        ),
      ),
    );
  }

  Future<void> _dialogCall(BuildContext context, String s) {
    var bytes = s;
    return showDialog(
        context: context,
        builder: (BuildContext context) {
          return CupertinoAlertDialog(
            content: Container(
              height: 250.0,
              width: 250.0,
              child: Image.memory(base64Decode(bytes)),
            ),
          );
        });
  }
}
