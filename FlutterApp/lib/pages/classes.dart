import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http_r_test/services/requests.dart';

class Class extends StatelessWidget {
  late String idRace;
  late String raceName;
  static String routeName = '/Classes';

  @override
  Widget build(BuildContext context) {
    var myArgument = (ModalRoute.of(context)?.settings.arguments) as List;
    this.idRace = myArgument[0];
    this.raceName = myArgument[1];
    return Scaffold(
      body: MyClassPage(idRace, raceName),
    );
  }
}

class MyClassPage extends StatefulWidget {
  late String idRace;
  late String raceName;

  MyClassPage(toSet0, toSet1) {
    idRace = toSet0;
    raceName = toSet1;
  }

  @override
  _MyClassPageState createState() => _MyClassPageState(idRace, raceName);
}

class _MyClassPageState extends State<MyClassPage> {
  late String idRace;
  late String raceName;

  _MyClassPageState(toSet0, toSet1) {
    this.idRace = toSet0;
    this.raceName = toSet1;
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
      final List newEntries = await Request.classRequest(idRace);
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
        middle: Text(raceName),
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
              onTap: () {},
            );
          }
        },
        controller: _scrollController,
      ),
    );
  }
}
