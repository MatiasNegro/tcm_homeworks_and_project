import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:FlutterApp/services/requests.dart';
import 'package:FlutterApp/pages/startGrid.dart';

class StartList extends StatelessWidget {
  late String idRace;
  late String className;
  static String routeName = '/Classes';

  @override
  Widget build(BuildContext context) {
    var myArgument = (ModalRoute.of(context)?.settings.arguments) as List;
    this.idRace = myArgument[0];
    this.className = myArgument[1];
    return Scaffold(
      body: MyStartListPage(idRace, className),
    );
  }
}

class MyStartListPage extends StatefulWidget {
  late String idRace;
  late String className;

  MyStartListPage(toSet0, toSet1) {
    idRace = toSet0;
    className = toSet1;
  }

  @override
  _MyStartListPageState createState() =>
      _MyStartListPageState(idRace, className);
}

class _MyStartListPageState extends State<MyStartListPage> {
  late String idRace;
  late String className;

  _MyStartListPageState(toSet0, toSet1) {
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
      final List newEntries = await Request.getStartListRequest(idRace);
      if (newEntries.isEmpty) {
        double edge = 50.0;
        double offsetFromBottom = _scrollController.position.maxScrollExtent -
            _scrollController.position.pixels;
        if (offsetFromBottom < edge) {
          _scrollController.animateTo(
              _scrollController.offset - (edge - offsetFromBottom),
              duration: Duration(milliseconds: 100),
              curve: Curves.easeOut);
        }
      }
      setState(() {
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
          opacity: isPerformingRequest ? 1.0 : 0.0,
          child: CircularProgressIndicator(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CupertinoNavigationBar(
        middle: Text(className),
      ),
      body: ListView.builder(
        itemCount: items.length + 1,
        itemBuilder: (context, index) {
          if (index == items.length) {
            return _buildProgressIndicator();
          } else {
            var toText = items[index];
            var id = toText['id'];
            var name = toText['Name'];
            return ListTile(
              title: Text(id),
              subtitle: Text(name),
              leading: const Icon(Icons.people_alt_rounded),
              onTap: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        settings:
                            RouteSettings(arguments: [idRace, toText['id']]),
                        builder: (context) => StartGrid()));
              },
            );
          }
        },
        controller: _scrollController,
      ),
    );
  }
}
