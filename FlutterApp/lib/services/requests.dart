import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
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

  static Future<bool> downloadFile(raceId) async {
    var toReturn = false;
    try {
      var status = await Permission.storage.request();
      if (status == PermissionStatus.granted) {
      } else if (status == PermissionStatus.denied) {
        print(
            'Permission denied. Show a dialog and again ask for the permission');
        return false;
      } else if (status == PermissionStatus.permanentlyDenied) {
        print('Take the user to the settings page.');
        await openAppSettings();
      }

      var dir = await getApplicationDocumentsDirectory();
      Response response = await Dio().request(apiUrlDownloadFile,
          options: Options(method: 'GET', responseType: ResponseType.plain),
          queryParameters: {'filename': raceId});
      var myFile = await File(dir.path + '/$raceId.xml').create();
      myFile.writeAsString(response.data);
      toReturn = true;
    } catch (e) {
      toReturn = false;
    }

    return toReturn;
  }
}
