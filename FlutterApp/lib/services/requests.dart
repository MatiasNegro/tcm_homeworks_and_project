import 'dart:convert';
import 'package:http/http.dart' as http;
import '../globals.dart';

class Request {
  static Future<List> raceNameRequest() async {
    final response = await http.get(Uri.parse(apiUrlListRaces));

    if (response.statusCode == 200) {
      // If the server did return a 200 OK response,
      // then parse the JSON.
      var raceList = [] as List;
      var myJson = jsonDecode(response.body) as Map;

      for (int i = 0; i < myJson.length; i++) {
        raceList.add(myJson[i.toString()]);
      }
      return raceList;
    } else {
      // If the server did not return a 200 OK response,
      // then throw an exception.
      throw Exception('Failed to load races names');
    }
  }

  static Future<List> classRequest(myParameter) async {
    final myQueryParameters = {'id': myParameter};
    final myUrl = apiUrlListCLasses + '?id=' + myParameter;
    final response = await http.get(Uri.parse(myUrl));
    if (response.statusCode == 200) {
      // If the server did return a 200 OK response,
      // then parse the JSON.
      List classList = [];
      var myJson = jsonDecode(response.body) as Map;
      for (int i = 0; i < myJson.length; i++) {
        classList.add(myJson['class' + '$i']);
      }
      return classList;
    } else {
      // If the server did not return a 200 OK response,
      // then throw an exception.
      throw Exception('Failed to load classes names');
    }
  }
}
