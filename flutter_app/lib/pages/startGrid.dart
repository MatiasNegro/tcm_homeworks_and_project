import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_app/services/requests.dart';

bool flag = true;

class StartGrid extends StatelessWidget {
  late String idRace;
  late String className;
  static String routeName = '/StartGrid';

  @override
  Widget build(BuildContext context) {
    var myArgument = (ModalRoute.of(context)?.settings.arguments) as List;
    this.idRace = myArgument[0];
    this.className = myArgument[1];
    return Scaffold(
      body: MyStartGridPage(idRace, className),
    );
  }
}

class MyStartGridPage extends StatefulWidget {
  late String idRace;
  late String className;

  MyStartGridPage(toSet0, toSet1) {
    idRace = toSet0;
    className = toSet1;
  }

  @override
  _MyStartGridPageState createState() =>
      _MyStartGridPageState(idRace, className);
}

class _MyStartGridPageState extends State<MyStartGridPage> {
  late String idRace;
  late String className;

  _MyStartGridPageState(toSet0, toSet1) {
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
          await Request.getStartGridOfRaceClass(idRace, className);
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
                leading: Icon(Icons.person),
                onTap: () {},
              );
            }
          },
          controller: _scrollController,
        ),
      ),
    );
  }
}
