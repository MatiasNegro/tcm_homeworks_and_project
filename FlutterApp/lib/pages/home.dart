import 'dart:io';
import 'package:FlutterApp/pages/startList.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:FlutterApp/globals.dart';
import 'package:FlutterApp/pages/classes.dart';
import 'package:FlutterApp/services/requests.dart';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:refresh_indicator_custom/refresh_indicator_custom.dart';

void main() => runApp(new Home());

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      theme: new ThemeData(primarySwatch: Colors.blue),
      home: new MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List items = [];
  ScrollController _scrollController = new ScrollController();
  bool isPerformingRequest = false;

  @override
  void initState() {
    super.initState();
    _getMoreData();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  _getMoreData() async {
    if (!isPerformingRequest) {
      setState(() => isPerformingRequest = true);
      final List newEntries = await Request.raceNameRequest();
      /*if (newEntries.isEmpty) {
        double edge = 50.0;
        double offsetFromBottom = _scrollController.position.maxScrollExtent -
            _scrollController.position.pixels;
        /*if (offsetFromBottom > edge) {
          _scrollController.animateTo(
              _scrollController.offset - (edge - offsetFromBottom),
              duration: Duration(milliseconds: 100),
              curve: Curves.easeOut);
        }*/
      }*/
      setState(() {
        items.clear();
        items.addAll(newEntries);
        isPerformingRequest = false;
      });
    }
  }

  void _showActionSheet(BuildContext context, raceId, raceName) {
    showCupertinoModalPopup<void>(
      context: context,
      builder: (BuildContext myContext) => CupertinoActionSheet(
        actions: <CupertinoActionSheetAction>[
          CupertinoActionSheetAction(
            /// This parameter indicates the action would be a default
            /// defualt behavior, turns the action's text to bold text.
            isDefaultAction: true,
            onPressed: () {
              Navigator.push(
                  context,
                  MaterialPageRoute(
                      settings: RouteSettings(arguments: [raceId, raceName]),
                      builder: (context) => new StartList()));
              Navigator.pop(myContext);
            },
            child: const Text('start list'),
          ),
          CupertinoActionSheetAction(
            isDefaultAction: true,
            onPressed: () {
              Navigator.push(
                  context,
                  MaterialPageRoute(
                      settings: RouteSettings(arguments: [raceId, raceName]),
                      builder: (context) => new Class()));
              Navigator.pop(myContext);
            },
            child: const Text('result list'),
          ),
        ],
      ),
    );
  }

  Widget _buildProgressIndicator() {
    double horSize = MediaQuery.of(context).size.width / 2;
    double verSize = MediaQuery.of(context).size.height / 2;
    return Padding(
      padding:
          EdgeInsets.symmetric(horizontal: horSize / 2, vertical: verSize / 2),
      child: Center(
        child: Opacity(
          opacity: isPerformingRequest ? 0.0 : 0.0,
          child: CircularProgressIndicator(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      edgeOffset: 100.0,
      onRefresh: () => _getMoreData(),
      child: Scaffold(
        appBar: const CupertinoNavigationBar(
          middle: Text("Race Manager"),
        ),
        body: ListView.builder(
          itemCount: items.length + 1,
          itemBuilder: (context, index) {
            if (index == items.length) {
              //items.clear();
              return _buildProgressIndicator();
            } else {
              var toText = items[index];
              var raceName = toText['race_name'];
              var raceDate = toText['race_date'];
              var raceId = toText['race_id'];
              return ListTile(
                title: Text("$raceName"),
                subtitle: Text("$raceDate"),
                leading: Icon(Icons.emoji_events, size: 45),
                trailing: ElevatedButton(
                  onPressed: () async {
                    Request.downloadFile(raceId);
                  },
                  child: Icon(
                    Icons.cloud_download,
                    size: 35,
                  ),
                  style: ButtonStyle(
                    shape: MaterialStateProperty.all(CircleBorder()),
                    padding: MaterialStateProperty.all(EdgeInsets.all(7)),
                    backgroundColor: MaterialStateProperty.all(
                        Colors.blue), // <-- Button color
                    overlayColor:
                        MaterialStateProperty.resolveWith<Color?>((states) {
                      if (states.contains(MaterialState.pressed))
                        return Colors.blue[50]; // <-- Splash color
                    }),
                  ),
                ),
                onTap: () {
                  _showActionSheet(context, raceId, raceName);
                },
              );
            }
          },
          controller: _scrollController,
        ),
      ),
    );
  }
}
