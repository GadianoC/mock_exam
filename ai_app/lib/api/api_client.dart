import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class ApiClient {
  final String _baseUrl = 'http://localhost:5000/api';

  Future<String> summarizeDocumentBytes(
    Uint8List fileBytes,
    double summaryLength,
    int detailLevel,
  ) async {
    final url = Uri.parse('$_baseUrl/summarize');
    final request = http.MultipartRequest('POST', url);

    request.files.add(
      http.MultipartFile.fromBytes(
        'document',
        fileBytes,
      ),
    );
    request.fields['summaryLength'] = summaryLength.toString();
    request.fields['detailLevel'] = detailLevel.toString();

    final http.StreamedResponse response = await request.send();

    print('Response status code: ${response.statusCode}');
    final responseData = await response.stream.bytesToString();

    if (response.statusCode == 200) {
      return jsonDecode(responseData)['summary'];
    } else {
      print('Error response: $responseData');
      throw Exception('Failed to summarize document: ${response.statusCode}');
    }
  }
}
